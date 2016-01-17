# Django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

# Project
from main.decorators import *

# Models
from db.models.message import Message
from db.models.forms import UserAccountForm
from db.models.warranty import Warranty
from db.models.warranty_image import WarrantyImage
from db.models.warranty_history import WarrantyHistory

# ---------------------------------------
#                 INDEX
# ---------------------------------------
@login_required
@eula_required
def index(request):
    if request.user.is_authenticated():
        user_profile = request.user.userprofile

        dashboard_messages = Message.objects.filter(Q(message_type="EVERYONE") |
                                              Q(message_type=user_profile.user_type)).filter(enabled=True).order_by("-message_date")

        return render_page(request, "main/index.html", "", {"dashboardMessages": dashboard_messages})


# ---------------------------------------
#                 EULA
# ---------------------------------------
@login_required
def eula(request):
    if request.method == "POST":
        user_profile = request.user.userprofile
        user_profile.eula_accepted = True
        user_profile.save()
        return HttpResponseRedirect("/")

    return render_page(request, "main/eula.html")


# ---------------------------------------
#             WARRANTY
# ---------------------------------------
@customer_service_required
def warranty(request, warranty_id):
    user_profile = request.user.userprofile

    if request.method == "POST":
        try:
            image_types = {
                "PROOF": "proof of purchase",
                "IMAGE": "product image"
            }

            file_type = request.POST.get("file_type", "IMAGE")
            description = request.POST.get("image_description", "")
            warranty = Warranty.objects.get(pk=warranty_id)
            count = 0
            for afile in request.FILES.getlist('files'):
                count += 1
                warranty_image = WarrantyImage(warranty=warranty,
                                               type=file_type,
                                               description=description,
                                               file_path=afile)
                warranty_image.save()

                action = "Uploaded '{}' as {}".format(afile, image_types[file_type])
                warranty_history = WarrantyHistory(warranty=warranty, user_profile=user_profile, action=action)
                warranty_history.save()

            if count > 0:
                messages.success(request, "Successfully uploaded file(s)!")
            else:
                messages.error(request, "No files were uploaded!")
        except Exception as e:
            messages.error(request, "Error uploading images!")

    return render_page(request, "main/warranty.html", "WARRANTY", {"warranty_id": warranty_id})


@customer_service_required
def warranty_new(request):
    user_profile = request.user.userprofile

    warranty = Warranty()
    warranty.save()
    warranty.claim_number = "CWC-{:04d}".format(warranty.pk)
    warranty.save()

    warranty_history = WarrantyHistory(warranty=warranty, user_profile=user_profile, action="New Claim")
    warranty_history.save()

    return HttpResponseRedirect("/warranty/{}/".format(warranty.pk))


@customer_service_required
def warranties(request):
    return render_page(request, "main/warranties.html")


@customer_service_required
def warranty_report(request):
    return render_page(request, "main/warranty_report.html")


# ---------------------------------------
#                EBRIDGE
# ---------------------------------------
@admin_required
def ebridge(request):
    return render_page(request, "main/ebridge.html", "ADMIN")


# ---------------------------------------
#                PROFILE
# ---------------------------------------
@login_required
def profile(request):
    user = request.user

    user_info = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                }

    check_errors = False
    if request.method == 'POST': # If a form has been submitted...
        if "old_password" in request.POST: #They submitted the password change form.
            account_form = UserAccountForm(user_info)
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()

                messages.success(request, "Password changed successfully.")

                return HttpResponseRedirect("/")
        else:
            check_errors = True
            # If they aren't changing their email, pass that to UserAccountForm.
            # This is so we can use form validation to ensure that new emails are unique. Since, if
            # it's unchanged it will obviously already exist and fail validation.
            if user.email == request.POST.get('email', ""):
                email_changed = False
            else:
                email_changed = True

            post = request.POST.copy()
            account_form = UserAccountForm(post, email_changed=email_changed)
            password_form = PasswordChangeForm(user)

            if account_form.is_valid():
                user.first_name = account_form.cleaned_data['first_name']
                user.last_name = account_form.cleaned_data['last_name']
                if email_changed:
                    user.email = account_form.cleaned_data['email']
                user.save()

                messages.success(request, "User information saved.")

                return HttpResponseRedirect("/")
    else:
        account_form = UserAccountForm(user_info)
        password_form = PasswordChangeForm(user)

    args = {
        "account_form": account_form,
        "password_form": password_form,
        "check_errors": check_errors,
    }

    return render_page(request, "main/profile.html", "", args)


# ---------------------------------------
#             RENDER PAGE
# ---------------------------------------
def render_page(request, page_template, page="", args={}):
    user_profile = request.user.userprofile
    
    default_args = {
        "user_profile": user_profile,
        "page": page,
    }
    default_args.update(args)
    
    return render(request, page_template, default_args)


# ---------------------------------------
#                HELPERS
# ---------------------------------------
def sub_domain(request):
    # Add sub domain to context.
    theme = "cobian"
    at_once_only = False
    fqdn = request.get_host().split(':')[0]

    # Break up the domain into parts and get the subdomain slug
    domain_parts = fqdn.split('.')
    if len(domain_parts) > 2:
        sub_domain = domain_parts[0].lower()
        if sub_domain == "ffsportal":
            theme = "flipflop"
            at_once_only = True
    
    return {"THEME": theme, "AT_ONCE_ONLY": at_once_only}