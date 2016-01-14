from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext
from datetime import datetime

from db.models.product_sku import ProductSku
from db.models.warranty import Warranty
from db.models.warranty_color import WarrantyColor
from db.models.warranty_history import WarrantyHistory
from db.models.warranty_image import WarrantyImage
from db.models.warranty_style import WarrantyStyle
from db.models.data_option import DataOption
from main.utils import make_html_email, send_email

# JSON
import json
import logging
import random

logger = logging.getLogger("portal.api.warranty")


def api_warranties(request):
    date_now = datetime.now()

    status = request.GET.get("status", "ALL")
    date_range = request.GET.get("date_range", "ALL")
    start_date = request.GET.get("start_date", "{}/{}/{}".format(date_now.month, date_now.day, date_now.year))
    end_date = request.GET.get("end_date", start_date)

    start_date_object = datetime.strptime("{} 12:01AM".format(start_date), '%m/%d/%Y %I:%M%p')
    end_date_object = datetime.strptime("{} 11:59PM".format(end_date), '%m/%d/%Y %I:%M%p')

    return_list = []
    try:
        warranties = Warranty.objects.all().order_by("-status_date")

        if status != "ALL":
            warranties = warranties.filter(status=status)

        if date_range != "ALL":
            warranties = warranties.filter(status_date__range=[start_date_object, end_date_object])

        for warranty in warranties:
            return_list.append(warranty.convert_to_dict())

    except Exception as e:
        logger.error("api_warranties: {}".format(e))

    return HttpResponse(json.dumps(return_list), mimetype="application/json")


def api_warranties_warranty(request, warranty_id):
    return_object = {}

    try:
        warranty = Warranty.objects.get(pk=warranty_id)

        if request.method == "GET":
            return_object = warranty.convert_to_dict()

        if request.method == "DELETE":
            warranty.delete()
            return_object = {"status": "deleted"}

    except Exception as e:
        logger.error("api_warranties_warranty: {}".format(e))
        return HttpResponseServerError("Error getting warranty data!")

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), mimetype="application/json")


def api_warranty_colors(request):
    return_list = []
    try:
        colors = WarrantyColor.objects.all().order_by("color")

        for color in colors:
            return_list.append(color.convert_to_dict())

    except Exception as e:
        logger.error("api_warranty_colors: {}".format(e))

    return HttpResponse(json.dumps(return_list), mimetype="application/json")


def api_warranty_defects(request):
    return_list = []
    try:
        defects = DataOption.objects.filter(option_type="WARRANTY_DAMAGE").order_by("description")

        for defect in defects:
            return_list.append(defect.convert_to_dict())

    except Exception as e:
        logger.error("api_warranty_defects: {}".format(e))

    return HttpResponse(json.dumps(return_list), mimetype="application/json")


def api_warranty_history(request, warranty_id):
    return_list = []
    try:
        warranty = Warranty.objects.get(pk=warranty_id)
        history = WarrantyHistory.objects.filter(warranty=warranty).order_by("action_date")
        for action in history:
            return_list.append(action.convert_to_dict())

    except Exception as e:
        logger.error("api_warranty_history: {}".format(e))

    return HttpResponse(json.dumps(return_list), mimetype="application/json")


def api_warranty_styles(request):
    return_list = []
    try:
        styles = WarrantyStyle.objects.all().order_by("style")

        for style in styles:
            return_list.append(style.convert_to_dict())

    except Exception as e:
        logger.error("api_warranty_styles: %s" % (e))

    return HttpResponse(json.dumps(return_list), mimetype="application/json")


def api_warranty(request, warranty_id):
    user_profile = request.user.get_profile()

    return_object = {}

    try:
        warranty = Warranty.objects.get(pk=warranty_id)
        warranty_dict = warranty.convert_to_dict()

        if request.method == "GET":
            return_object = warranty.convert_to_dict()

        if request.method == "POST":
            return_status = "success"
            actions = []
            before_status = warranty.status
            before_status_description = None
            model_json = request.POST.get("model", None)
            model = json.loads(model_json)
            if warranty.status != model["status"]:
                before_status_description = warranty_dict["statusDescription"]
                warranty.status = model["status"]
                warranty.status_date = datetime.now()

            if warranty.name != model["name"]:
                actions.append("Changed name '{}' to '{}'".format(warranty.name, model["name"]))
                warranty.name = model["name"]

            if warranty.email != model["email"]:
                actions.append("Changed email '{}' to '{}'".format(warranty.email, model["email"]))
                warranty.email = model["email"]

            if warranty.phone != model["phone"]:
                actions.append("Changed phone '{}' to '{}'".format(warranty.phone, model["phone"]))
                warranty.phone = model["phone"]

            if warranty.address != model["address"]:
                actions.append("Changed address '{}' to '{}'".format(warranty.address, model["address"]))
                warranty.address = model["address"]

            if warranty.style != model["style"]:
                actions.append("Changed style '{}' to '{}'".format(warranty.style, model["style"]))
                warranty.style = model["style"]

            if warranty.color != model["color"]:
                actions.append("Changed color '{}' to '{}'".format(warranty.color, model["color"]))
                warranty.color = model["color"]

            if warranty.damage != model["damage"]:
                actions.append("Changed damage '{}' to '{}'".format(warranty.damage, model["damage"]))
                warranty.damage = model["damage"]

            warranty.notes = model["notes"]
            if model["imageOverride"]:
                if not warranty.image_override:
                    actions.append("Set 'Image Override' to True")
                    warranty.image_override = True
            else:
                if warranty.image_override:
                    actions.append("Set 'Image Override' to False")
                    warranty.image_override = False

            warranty.save()
            warranty_dict = warranty.convert_to_dict()

            if before_status_description:
                actions.append("Changed status '{}' to '{}'".format(before_status_description,
                                                                    warranty_dict["statusDescription"]))

            if warranty.status == "PREAUTHORIZED" and not warranty.email_sent:
                if send_pre_authorized_email(request, warranty):
                    warranty.email_sent = True
                    warranty.save()
                    actions.append("Pre-authorized email sent")
                else:
                    return_status = "Error sending email, status not changed"
                    warranty.status = before_status
                    warranty.save()
                    actions.append("ERROR Sending Pre-authorized email!")

            for action in actions:
                warranty_history = WarrantyHistory(warranty=warranty, user_profile=user_profile, action=action)
                warranty_history.save()

            return_object = {
                "returnStatus": return_status,
                "model": warranty_dict,
            }

        if request.method == "DELETE":
            warranty.delete()
            return_object = {"status": "deleted"}

    except Exception as e:
        logger.error("api_warranty: %s" % (e))
        return HttpResponseServerError("Error getting warranty data!")

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), mimetype="application/json")


def api_warranty_status(request, warranty_id):
    user_profile = request.user.get_profile()

    return_object = {}

    try:
        warranty = Warranty.objects.get(pk=warranty_id)
        warranty_dict = warranty.convert_to_dict()

        if request.method == "GET":

            return_object["status"] = warranty_dict["status"]

        if request.method == "POST":
            model_json = request.POST.get("model", None)
            model = json.loads(model_json)

            if warranty.status != model["status"]:
                from_status = warranty_dict["statusDescription"]

                warranty.status = model["status"]
                warranty.status_date = datetime.now()
                warranty.save()

                warranty_dict = warranty.convert_to_dict()

                action = "Changed status from '{}' to '{}'".format(from_status, warranty_dict["statusDescription"])
                warranty_history = WarrantyHistory(warranty=warranty, user_profile=user_profile, action=action)
                warranty_history.save()

            return_object = {
                "model": warranty_dict,
            }

    except Exception as e:
        logger.error("api_warranty_set_status: %s" % (e))
        return HttpResponseServerError("Error saving warranty status!")

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), mimetype="application/json")


def api_warranty_images(request, warranty_id):
    return_list = []

    try:
        warranty = Warranty.objects.get(pk=warranty_id)
        for warranty_image in warranty.images.all():
            return_list.append(warranty_image.convert_to_dict())

    except Exception as e:
        logger.error("api_warranty_images: %s" % (e))
        return HttpResponseServerError("Error getting warranty images!")

    return HttpResponse(json.dumps(return_list, separators=(',', ':')), mimetype="application/json")


def api_warranty_images_image(request, warranty_id, warranty_image_id):
    user_profile = request.user.get_profile()

    return_object = {}

    try:
        warranty_image = WarrantyImage.objects.get(pk=warranty_image_id)
        warranty_image_dict = warranty_image.convert_to_dict()

        if request.method == "DELETE":
            action = "Removed '{}' image '{}'".format(warranty_image_dict["typeDescription"],
                                                      warranty_image_dict["fileName"])
            warranty_history = WarrantyHistory(warranty=warranty_image.warranty,
                                               user_profile=user_profile,
                                               action=action)
            warranty_history.save()

            warranty_image.delete()
            return_object = {"status": "deleted"}
        else:
            return_object = warranty_image_dict

    except Exception as e:
        logger.error("api_warranty_images_image: %s" % (e))
        return HttpResponseServerError("Error getting warranty images!")

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), mimetype="application/json")


def send_pre_authorized_email(request, warranty):
    user_profile = request.user.get_profile()
    email = user_profile.user.email

    emails = [email, warranty.email]
    email_subject = "Cobian Warranty Claim"
    email_body = make_html_email('emails/warranty_pre_authorized',
                                 {"warranty": warranty},
                                 context_instance=RequestContext(request))

    return send_email(email_subject, email_body, emails)


def api_warranty_create_data(request):
    skus = ProductSku.objects.all()

    color_dict = {}
    style_dict = {}

    for sku in skus:
        if sku.description not in color_dict:
            color_dict[sku.description] = 1

        if sku.style not in style_dict:
            style_dict[sku.style] = 1

    return_object = {"colors": [], "styles": [], "damages": []}

    for key in color_dict:
        return_object["colors"].append(key)
        wc = WarrantyColor(color=key)
        wc.save()

    for key in style_dict:
        return_object["styles"].append(key)
        ws = WarrantyStyle(style=key)
        ws.save()

    damages = [
        "Broken Strap",
        "Crushed",
        "Curled",
        "Delaminated Layers",
        "Discolored",
        "Toe Post Pulled Out",
        "Torn Strap",
        "Worn / Cracked Top Sole"
    ]

    sort_order = -1
    for damage in damages:
        sort_order += 1
        data_option = DataOption(option_type="WARRANTY_DAMAGE",
                                 description=damage,
                                 value=damage,
                                 sort_order=sort_order)
        data_option.save()
        return_object["damages"].append(data_option.convert_to_dict())

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), mimetype="application/json")


def api_warranty_create_claims(request):
    user_profile = request.user.get_profile()

    count = int(request.GET.get("count", "10"))

    statuses = ["NEW", "PREAUTHORIZED", "RECEIVED", "AUTHORIZED", "NOTAUTHORIZED", "CLOSED"]
    styles = ["Afina", "Bachelor", "Cali", "Dakota", "Eden", "Faux Nias", "Grace", "Huntington", "Ivana", "Jaida"]
    colors = ["Africa", "Black", "Camo", "Denim", "Emerald", "Flannel", "Gray", "Hope Brown", "Java", "Kameleon"]
    damages = ["Broken Strap", "Crushed", "Curled", "Delaminated Layers", "Discolored", "Toe Post Pulled Out",
               "Torn Strap", "Worn / Cracked Top Sole"]

    return_list = []
    for i in range(1, count + 1):
        year = random.randint(2015, 2016)
        month = 1
        day = random.randint(1, 9)
        if year == 2015:
            month = random.randint(1, 12)
            day = random.randint(1, 28)

        status = statuses[random.randint(0, 5)]
        status_date = datetime.strptime("{}/{}/{}".format(month, day, year), '%m/%d/%Y')
        name = "Name {}".format(i)
        email = "bridepeello@gmail.com"
        phone = "Phone {}".format(i)
        address = "Address {}".format(i)
        style = styles[random.randint(0, 9)]
        color = colors[random.randint(0, 9)]
        damage = damages[random.randint(0, 7)]

        warranty = Warranty()
        warranty.save()

        warranty.claim_number = "CWC-{:04d}".format(warranty.pk)
        warranty.status = status
        warranty.status_date = status_date
        warranty.name = name
        warranty.email = email
        warranty.phone = phone
        warranty.address = address
        warranty.style = style
        warranty.color = color
        warranty.damage = damage
        warranty.save()

        warranty_dict = warranty.convert_to_dict()
        return_list.append(warranty_dict)

        warranty_history = WarrantyHistory(warranty=warranty, user_profile=user_profile, action="New claim")
        warranty_history.save()

        if status != "NEW":
            warranty_history = WarrantyHistory(warranty=warranty,
                                               user_profile=user_profile,
                                               action="Set status to {}".format(warranty_dict["statusDescription"]))
            warranty_history.save()

    return HttpResponse(json.dumps(return_list, separators=(',', ':')), mimetype="application/json")
