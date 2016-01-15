from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    user_profile = None
    if request.user.is_authenticated():
        user_profile = request.user.userprofile
        messages = Message.objects.filter(Q(message_type="EVERYONE") | Q(message_type=user_profile.user_type)).filter(enabled=True).order_by("-message_date")
        return render_page(request, "main/index.html", "", {"messages": messages})


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
    # Adds the base url to the context.
    base_url = "" #settings.URL_BASE
    
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
    
    print("THEME: {0}".format(theme))
    
    return {"THEME": theme, "AT_ONCE_ONLY": at_once_only}