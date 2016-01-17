# DJANGO
from django.http import HttpResponse,HttpResponseServerError
from django.conf import settings
from django.template import RequestContext
from datetime import datetime, timedelta
from dateutil.parser import parse

# MODELS
from db.models.user_profile import User, UserProfile

from db.order_factory import get_default_data_option, send_order
from main.utils import make_both_emails, send_email_safe, make_html_email, send_email

# CSV
import csv

# JSON
import ujson as json

import logging

logger = logging.getLogger("portal.api.views")


# ------------------------------------------
#                DEALERS
# ------------------------------------------
def api_dealers(request):
    rep_id = int(request.GET.get("rep_id", "0"))

    return_list = []
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type == "DEALER":
            return_list.append(user_profile.convert_to_dict())
        else:
            dealers = UserProfile.objects.filter(user_type="DEALER").order_by("account_id")
            if user_profile.user_type == "REP":
                dealers = dealers.filter(account_rep__pk=user_profile.pk)
            elif rep_id > 0:
                dealers = dealers.filter(account_rep__pk=rep_id)

            for dealer in dealers:
                return_list.append(dealer.convert_to_dict())

    except Exception as e:
        logger.error("api_dealers: %s" % (e))

    return HttpResponse(json.dumps(return_list), content_type="application/json")


def api_dealer(request, dealer_id):
    return_object = {}
    try:
        dealer = UserProfile.objects.get(pk=dealer_id)
        return_object = dealer.convert_to_dict()

    except Exception as e:
        logger.error("api_dealer: %s" % (e))

    return HttpResponse(json.dumps(return_object), content_type="application/json")


def api_dealers_create(request):
    return_list = []
    f = open("/Users/peello/Downloads/dealers.txt")
    for line in f:
        line_split = line.split("|")
        dealer_dict = {
            "id": int(line_split[0]),
            "userId": int(line_split[1]),
            "repAccountId": line_split[2],
            "accountId": line_split[3],
            "company": line_split[4]
        }
        return_list.append(dealer_dict)

        rep_exists = False
        try:
            rep = UserProfile.objects.get(account_id=dealer_dict["repAccountId"])
            rep_exists = True

        except Exception as e:
            print("  ** REP NOT FOUND - {}".format(dealer_dict["repAccountId"]))

        if rep_exists:
            try:
                user = User(username=dealer_dict["accountId"], is_staff=False, is_active=True, is_superuser=False)
                user.set_password(dealer_dict["accountId"])
                user.save()

                user_profile = UserProfile(user=user,
                                           account_rep=rep,
                                           user_type="DEALER",
                                           account_id=dealer_dict["accountId"],
                                           company=dealer_dict["company"])
                user_profile.save()
                print("  ** CREATED - UserId (%s)  UserProfileId (%s)" % (user.pk, user_profile.pk))
            except Exception as e:
                print("  ** ERROR - %s : %s" % (dealer_dict["accountId"], e))
    f.close()

    return HttpResponse(json.dumps(return_list), content_type="application/json")

# ------------------------------------------
#                  REPS
# ------------------------------------------
def api_reps(request):
    return_list = []
    try:
        user_profile = request.user.userprofile
        if user_profile.user_type == "REP":
            return_list.append(user_profile.convert_to_dict())
        elif user_profile.user_type == "DEALER":
            rep_user_profile = UserProfile.objects.get(pk=user_profile.account_rep.pk)
            return_list.append(rep_user_profile.convert_to_dict())
        else:
            for rep_user_profile in UserProfile.objects.filter(user_type="REP").order_by("account_id"):
                return_list.append(rep_user_profile.convert_to_dict())

    except Exception as e:
        logger.error("api_reps: {}".format(e))
        return HttpResponseServerError(e)

    return HttpResponse(json.dumps(return_list), content_type="application/json")


def api_rep(request, rep_id):
    return_object = {}
    try:
        dealer = UserProfile.objects.get(pk=rep_id)
        return_object = dealer.convert_to_dict()

    except Exception as e:
        logger.error("api_rep: %s" % (e))

    return HttpResponse(json.dumps(return_object), content_type="application/json")


def api_reps_create(request):
    rep_list = []
    rep_list.append({"company": "Raz Hodgeman", "first_name": "Raz", "last_name": "Hodgeman", "account_id": "056", "email": "razhodg@gmail.com", "phone": "949-374-4011"})
    rep_list.append({"company": "Raz Hodgeman", "first_name": "Raz", "last_name": "Hodgeman", "account_id": "058", "email": "razhodg@gmail.com", "phone": "949-374-4011"})
    rep_list.append({"company": "Mike Burns", "first_name": "Mike", "last_name": "Burns", "account_id": "041", "email": "mburns.oniell@cox.net", "phone": "760-473-7445"})
    rep_list.append({"company": "Greg Taylor (GT)", "first_name": "Greg", "last_name": "Taylor", "account_id": "051", "email": "gt@gtsurflines.com", "phone": "904-806-4169"})
    rep_list.append({"company": "Greg Taylor (GT)", "first_name": "Greg", "last_name": "Taylor", "account_id": "052", "email": "gt@gtsurflines.com", "phone": "904-806-4169"})
    rep_list.append({"company": "Ernie Yagi", "first_name": "Ernie", "last_name": "Yagi", "account_id": "005", "email": "ernie@surfstuff.net", "phone": "808-479-9343"})
    rep_list.append({"company": "Mark Neustadter", "first_name": "Mark", "last_name": "Neustadter", "account_id": "039", "email": "newtz2@aol.com", "phone": "609-442-4009"})
    rep_list.append({"company": "Lance & Amy Gilman", "first_name": "Lance", "last_name": "Gilman", "account_id": "055", "email": "lg93@me.com", "phone": "702-862-9095"})
    rep_list.append({"company": "Brian Jolin", "first_name": "Brian", "last_name": "Jolin", "account_id": "035", "email": "brian@jolin.org", "phone": "817-368-3061"})
    rep_list.append({"company": "Karen Moldstad", "first_name": "Karen", "last_name": "Moldstad", "account_id": "009", "email": "kjmold@earthlink.net", "phone": "206-295-5626"})
    rep_list.append({"company": "Rose Macke", "first_name": "Rose", "last_name": "Macke", "account_id": "024", "email": "mackeclan@cox.", "phone": "949-433-1626"})
    rep_list.append({"company": "Paul Kuchno", "first_name": "Paul", "last_name": "Kuchno", "account_id": "080", "email": "pgkuchno@hotmail.com", "phone": "787-603-8535"})
    rep_list.append({"company": "Kevin Campion", "first_name": "Kevin", "last_name": "Campion", "account_id": "085", "email": "anarchy@impulse.net", "phone": "805-550-5562"})
    rep_list.append({"company": "Jeff Clark", "first_name": "Jeff", "last_name": "Clark", "account_id": "083", "email": "jeffclark9@juno.com", "phone": "503-706-1775"})
    rep_list.append({"company": "Marc Angelillo", "first_name": "Marc", "last_name": "Angelillo", "account_id": "029", "email": "m.angelillo@att.net", "phone": "617-842-9705"})
    rep_list.append({"company": "Barry Mayers", "first_name": "Barry", "last_name": "Mayers", "account_id": "115", "email": "barry_mayers@hotmail.com", "phone": "246-428-4390"})
    rep_list.append({"company": "Gabriella", "first_name": "Gabriella", "last_name": "", "account_id": "106", "email": "gabrielarichards@gmail.com", "phone": "599-767-2252"})
    rep_list.append({"company": "PJ Bahama", "first_name": "PJ", "last_name": "Bahama", "account_id": "111", "email": "pjbahamas@batelnet.bs", "phone": "242-394-3910"})
    rep_list.append({"company": "Geary Guay", "first_name": "Geary", "last_name": "Guay", "account_id": "025", "email": "geary@outdoorsalesrep.com", "phone": "303-517-9928"})
    rep_list.append({"company": "Sheri Letow", "first_name": "Sheri", "last_name": "Letow", "account_id": "078", "email": "sheriletow@gmail.com", "phone": "469-366-1518"})

    count = 0
    for rep in rep_list:
        count += 1

        print("%s - %s : %s" % (count, rep["account_id"], rep["company"]))

        create_rep = False
        try:
            user = User.objects.get(username=rep["account_id"])
            user.first_name = rep["first_name"]
            user.last_name = rep["last_name"]
            user.email = rep["email"]
            user.save()

            user_profile = UserProfile.objects.get(user=user)
            user_profile.company = rep["company"]
            user_profile.phone = rep["phone"]
            user_profile.save()

            print("  ** FOUND - UserId (%s)  UserProfileId (%s)" % (user.pk, user_profile.pk))

        except Exception as e:
            print("  ** NOT FOUND - %s" % (e))
            create_rep = True

        if create_rep:
            try:
                user = User(username=rep["account_id"], is_staff=False, is_active=True, is_superuser=False)
                user.set_password(rep["account_id"])
                user.first_name = rep["first_name"]
                user.last_name = rep["last_name"]
                user.email = rep["email"]
                user.save()

                user_profile = UserProfile(user=user, user_type="REP", account_id=rep["account_id"], company=rep["company"], phone=rep["phone"])
                user_profile.save()
                print("  ** CREATED - UserId (%s)  UserProfileId (%s)" % (user.pk, user_profile.pk))
            except Exception as e:
                print("  ** ERROR - import_rep (%s) : %s" % (rep["account_id"], e))

    return HttpResponse(json.dumps(rep_list), content_type="application/json")


# ------------------------------------------
#             MODEL INVENTORY
# ------------------------------------------
def api_model_inventory_list(request, dealer_id):
    try:
        return_list = []
        user_profile = UserProfile.objects.get(pk=dealer_id)
        for model_inventory in ModelInventory.objects.filter(user_profile=user_profile):
            return_list.append(model_inventory.convert_to_dict())

        return HttpResponse(json.dumps(return_list), content_type="application/json")

    except Exception as e:
        logger.error("api_dealer_model_inventory: %s" % (e))
        return HttpResponseServerError(e)


def api_model_inventory_create(request, dealer_id):
    try:
        return_object = {}
        if request.method == "POST":
            model_json = request.POST.get("modelSku", None)
            user_profile = UserProfile.objects.get(pk=dealer_id)
            return_object = user_profile.convert_to_dict()

        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_dealer_model_inventory: %s" % (e))
        return HttpResponseServerError(e)


def api_model_inventory(request, dealer_id, model_inventory_id):
    return_object = {}

    try:
        model_inventory = ModelInventory.objects.get(pk=model_inventory_id)

        # Get
        if request.method == "GET":
            return_object = model_inventory.convert_to_dict()

        # Delete
        if request.method == "DELETE":
            model_inventory.delete()
            return_object = {"status": "deleted"}

        # Duplicate   
        if request.method == "PATCH":
            model_inventory.pk = None
            model_inventory.save()
            return_object = model_inventory.convert_to_dict()

        # Update
        if request.method == "PUT":
            model_json = json.loads(request.body)
            return_object = model_inventory.convert_to_dict()

    except Exception as e:
        logger.error("api_model_inventory: %s" % (e))
        return HttpResponseServerError("Error getting model data!")

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), content_type="application/json")


# ------------------------------------------
#                INVENTORY
# ------------------------------------------
def api_inventory(request):
    return_list = []
    try:
        csv_file_path = "%scobian_inventory.csv" % (settings.MEDIA_ROOT)
        with open(csv_file_path, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in csv_reader:
                try:
                    return_list.append({
                        "sku": row[0],
                        "inStock": int(row[1])
                    })
                except Exception as e:
                    pass

    except Exception as e:
        logger.error("api_inventory: %s" % (e))

    return HttpResponse(json.dumps(return_list), content_type="application/json")


# ------------------------------------------
#                ORDERS
# ------------------------------------------
def api_orders(request):
    date_now = datetime.now()

    rep_id = int(request.GET.get("rep_id", "0"))
    dealer_id = int(request.GET.get("dealer_id", "0"))
    order_type = request.GET.get("type", "ALL")
    status = request.GET.get("status", "ALL")
    date_range = request.GET.get("date_range", "ALL")
    start_date = request.GET.get("start_date", "%s/%s/%s" % (date_now.month, date_now.day, date_now.year))
    end_date = request.GET.get("end_date", start_date)

    start_date_object = datetime.strptime('%s 12:01AM' % (start_date), '%m/%d/%Y %I:%M%p')
    end_date_object = datetime.strptime('%s 11:59PM' % (end_date), '%m/%d/%Y %I:%M%p')

    return_list = []
    try:
        orders = Order.objects.all().order_by("-status_date")

        if order_type != "ALL":
            orders = orders.filter(order_type=order_type)

        if status != "ALL":
            orders = orders.filter(status=status)

        if date_range != "ALL":
            orders = orders.filter(status_date__range=[start_date_object, end_date_object])

        if rep_id > 0:
            orders = orders.filter(user_profile__account_rep__pk=rep_id)

        if dealer_id > 0:
            orders = orders.filter(user_profile__pk=dealer_id)

        for order in orders:
            # print "---- order ----"
            # print "  OrderId: %s" % order.pk

            total = 0
            for order_detail in order.order_details.all():
                total += order_detail.quantity * order_detail.price

            order_status = order.status
            for value, description in Order.ORDER_STATUS:
                if value == order.status:
                    order_status = description
                    continue

            order_type = order.order_type
            for value, description in Order.ORDER_TYPE:
                if value == order_type:
                    order_type = description
                    continue

            order_dict = {
                "id": order.pk,
                "orderNumber": order.pk,
                "poNumber": order.po_number,
                "repId": order.user_profile.account_rep.pk,
                "repAccountId": order.user_profile.account_rep.account_id,
                "dealerId": order.user_profile.pk,
                "dealerAccountId": order.user_profile.account_id,
                "dealer": order.user_profile.company,
                "orderDate": "%s/%s/%s" % (order.order_date.month, order.order_date.day, order.order_date.year),
                "statusDate": "%s/%s/%s" % (order.status_date.month, order.status_date.day, order.status_date.year),
                "status": order_status,
                "orderType": order_type,
                "total": "%.2f" % (total)
            }
            # print order_dict
            return_list.append(order_dict)

    except Exception as e:
        logger.error("api_orders: %s" % (e))

    return HttpResponse(json.dumps(return_list), content_type="application/json")


def api_order(request, order_id):
    return_object = {}

    try:
        if request.method == "GET":
            order = Order.objects.get(pk=order_id)
            return_object = order.convert_to_dict();

        if request.method == "DELETE":
            order = Order.objects.get(pk=order_id)
            order.delete()
            return_object = {"status": "deleted"}

        if request.method == "PATCH":
            return_object = order_duplicate(order_id)

    except Exception as e:
        logger.error("api_order: %s" % (e))
        return HttpResponseServerError("Error getting order data!")

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), content_type="application/json")


def api_order_details(request, order_id):
    return_object = []

    try:
        order_details = OrderDetail.objects.filter(order__pk=order_id).order_by("sku")
        for order_detail in order_details:
            return_object.append(order_detail.convert_to_dict())

    except Exception as e:
        logger.error("api_order_details: %s" % (e))
        return HttpResponseServerError("Error getting order data: %s" % (e))

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), content_type="application/json")


def api_order_detail(request, order_id, order_detail_id):
    return_object = {}

    try:
        order_detail = OrderDetail.objects.get(pk=order_detail_id)
        return_object = order_detail.convert_to_dict()

    except Exception as e:
        logger.error("api_order_details: %s" % (e))
        return HttpResponseServerError("Error getting order data: %s" % (e))

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), content_type="application/json")


def api_order_data(request, order_id):
    return_object = {
        "order": {},
        "details": [],
        "styles": [],
    }
    styles = []
    try:
        order = Order.objects.get(pk=order_id)
        return_object["order"] = order.convert_to_dict()

        order_details = OrderDetail.objects.filter(order=order).order_by("sku")
        for order_detail in order_details:
            return_object["details"].append(order_detail.convert_to_dict())

            try:
                style_sku = order_detail.sku[:order_detail.sku.find("-")]
                if style_sku not in styles:
                    styles.append(style_sku)
                    product_style_id = product_style_get_id(style_sku)
                    return_object["styles"].append(product_style_detail(product_style_id))

            except Exception as e:
                pass

    except Exception as e:
        logger.error("api_order_data: %s" % (e))
        return HttpResponseServerError("Error getting order data: %s" % (e))

    return HttpResponse(json.dumps(return_object, separators=(',', ':')), content_type="application/json")


def api_order_new(request):
    try:
        user_profile = request.user.userprofile

        dealer_id = int(request.GET.get("dealer_id", "0"))
        dealer = UserProfile.objects.get(pk=dealer_id)

        order = Order(user_profile=dealer, status='NEW')
        order.order_type = "AT-ONCE"
        order.prebook_date = datetime.now()
        order.cancel_date = datetime.now() + timedelta(days=30)
        order.pre_book_option = get_default_data_option("PRE-BOOK")
        if user_profile.user_type == "DEALER":
            order.order_source = "BUYER"
        else:
            order.order_source = "NONE"

        order.billto_phone = dealer.phone
        order.billto_email = dealer.user.email
        order.shipto_phone = dealer.phone
        order.shipto_email = dealer.user.email

        try:
            billto_address = UserAddress.objects.filter(user_profile=dealer, address_type="BILLTO")[0]

            if billto_address.name:
                order.billto_name = billto_address.name
            else:
                order.billto_name = dealer.company

            order.billto_address1 = billto_address.address1
            order.billto_address2 = billto_address.address2
            order.billto_city = billto_address.city
            order.billto_state = billto_address.state
            order.billto_postal_code = billto_address.postal_code
            order.billto_country = billto_address.country
        except Exception as e:
            pass

        try:
            shipto_address = UserAddress.objects.filter(user_profile=dealer, address_type="SHIPTO")[0]

            if shipto_address.name:
                order.shipto_name = shipto_address.name
            else:
                order.shipto_name = dealer.company

            order.shipto_address_id = shipto_address.address_id
            order.shipto_address1 = shipto_address.address1
            order.shipto_address2 = shipto_address.address2
            order.shipto_city = shipto_address.city
            order.shipto_state = shipto_address.state
            order.shipto_postal_code = shipto_address.postal_code
            order.shipto_country = shipto_address.country
        except:
            pass

        order.save()

        # Create default PO#
        order.po_number = "%s-%s" % (dealer.account_id, order.pk)
        order.save()

        return HttpResponse(json.dumps({"id": order.pk}), content_type="application/json")

    except Exception as e:
        logger.error("api_order_new: %s" % (e))
        return HttpResponseServerError(e)


def api_order_duplicate(request):
    try:
        order_id = int(request.GET.get("order_id", "0"))
        return_object = order_duplicate(order_id)
        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_order_duplicate: %s" % (e))
        return HttpResponseServerError(e)


def api_order_save(request, order_id):
    order_json = request.POST.get("model", None)

    if order_json:
        try:
            order_dict = json.loads(order_json)

            # print("---------- order_dict before ----------")
            # print(order_dict)
            # print("---------------------------------------")

            order = Order.objects.get(pk=int(order_id))
            order.po_number = order_dict["poNumber"]
            order.order_type = order_dict["orderType"]
            order.order_source = order_dict["orderSource"]
            order.notes = order_dict["notes"]

            try:
                if valid_date(order_dict["preBookDate"]):
                    order.prebook_date = parse(order_dict["preBookDate"])
            except Exception as e:
                pass

            try:
                if valid_date(order_dict["cancelDate"]):
                    order.cancel_date = parse(order_dict["cancelDate"])
            except Exception as e:
                pass

            try:
                order.pre_book_option = order_dict["preBookOption"]
            except Exception as e:
                pass

            if order_dict["shipToId"] > 0:
                try:
                    shipto_address = UserAddress.objects.get(pk=order_dict["shipToId"])
                    order.shipto_name = shipto_address.name
                    order.shipto_address_id = shipto_address.address_id
                    order.shipto_address1 = shipto_address.address1
                    order.shipto_address2 = shipto_address.address2
                    order.shipto_city = shipto_address.city
                    order.shipto_state = shipto_address.state
                    order.shipto_postal_code = shipto_address.postal_code
                    order.shipto_country = shipto_address.country
                except:
                    pass

            order.save()

            for order_item in order_dict["orderItems"]:
                order_detail_id = order_item["odid"]

                if order_detail_id == 0:
                    product_sku = ProductSku.objects.get(pk=order_item["id"])
                    order_detail = OrderDetail(
                        order=order,
                        quantity=order_item["quantity"],
                        sku=product_sku.sku,
                        item_number=product_sku.item_number,
                        style=product_sku.style,
                        description=product_sku.description,
                        size=product_sku.size,
                        upc=product_sku.upc,
                        cost=product_sku.cost,
                        price=product_sku.wholesale
                    )
                    order_detail.save()
                    order_item["odid"] = order_detail.pk
                else:
                    order_detail = OrderDetail.objects.get(pk=order_detail_id)
                    if order_item["quantity"] > 0:
                        order_detail.quantity = order_item["quantity"]
                        order_detail.save()
                    else:
                        order_detail.delete()

            # print("---------- order_dict after ----------")
            # print(order_dict)
            # print("--------------------------------------")

            return HttpResponse(json.dumps(order_dict), content_type="application/json")

        except Exception as e:
            logger.error("api_order_save: %s" % (e))
            return HttpResponseServerError(e)
    else:
        return HttpResponseServerError("Invalid order format!")


def api_order_submit(request, order_id):
    if send_order(order_id):
        order = Order.objects.get(pk=order_id)
        order.status = "SUBMIT"
        order.status_date = datetime.now()
        order.save()

        email_sent = email_submitted_order(request, order_id)

        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
    else:
        return HttpResponseServerError("Failed to submit order!")


def api_order_email(request, order_id):
    user_profile = request.user.userprofile
    email = user_profile.user.email

    if order_email(request, email, order_id):
        return HttpResponse(json.dumps({"status": "success", "message": "Email has been sent to %s" % (email)}),
                            content_type="application/json")
    else:
        return HttpResponseServerError("Failed to email order!")


def order_duplicate(order_id):
    try:
        original_order = Order.objects.get(pk=order_id)
        original_order_details = original_order.order_details.all()
        po_number = "%s - copy" % (original_order.po_number)
        new_order = original_order
        new_order.pk = None
        new_order.status = "NEW"
        new_order.po_number = po_number
        new_order.order_date = datetime.now()
        new_order.status_date = datetime.now()
        new_order.prebook_date = datetime.now() + timedelta(days=90)
        new_order.cancel_date = datetime.now() + timedelta(days=120)

        dealer = original_order.user_profile

        new_order.billto_phone = dealer.phone
        new_order.billto_email = dealer.user.email
        new_order.shipto_phone = dealer.phone
        new_order.shipto_email = dealer.user.email

        try:
            billto_address = UserAddress.objects.filter(user_profile=dealer, address_type="BILLTO")[0]

            if billto_address.name:
                new_order.billto_name = billto_address.name
            else:
                new_order.billto_name = dealer.company

            new_order.billto_address1 = billto_address.address1
            new_order.billto_address2 = billto_address.address2
            new_order.billto_city = billto_address.city
            new_order.billto_state = billto_address.state
            new_order.billto_postal_code = billto_address.postal_code
            new_order.billto_country = billto_address.country
        except Exception as e:
            pass

        try:
            shipto_address = UserAddress.objects.filter(user_profile=dealer, address_type="SHIPTO")[0]

            if shipto_address.name:
                new_order.shipto_name = shipto_address.name
            else:
                new_order.shipto_name = dealer.company

            new_order.shipto_address_id = shipto_address.address_id
            new_order.shipto_address1 = shipto_address.address1
            new_order.shipto_address2 = shipto_address.address2
            new_order.shipto_city = shipto_address.city
            new_order.shipto_state = shipto_address.state
            new_order.shipto_postal_code = shipto_address.postal_code
            new_order.shipto_country = shipto_address.country
        except:
            pass

        new_order.save()

        inactive_skus = []
        for original_order_detail in original_order_details:
            if sku_exists(original_order_detail.sku):
                new_order_detail = original_order_detail
                new_order_detail.pk = None
                new_order_detail.order = new_order
                new_order_detail.save()
            else:
                inactive_skus.append(original_order_detail.sku)

        if len(inactive_skus) > 0:
            title = "Inactive Skus from order #%s" % (order_id)
            notes = "%s\r\n\r\n%s" % (new_order.notes, title)
            for sku in inactive_skus:
                notes = "%s\r\n%s" % (notes, sku)
            new_order.notes = notes
            new_order.save()

        return_object = {
            "status": "success",
            "order_id": new_order.pk,
            "po_number": po_number,
            "inactive_skus": inactive_skus
        }

        return return_object

    except Exception as e:
        logger.error("order_duplicate: %s" % (e))
        raise e


def api_order_sources(request):
    order_sources = []
    try:
        user_profile = request.user.userprofile
        # if user_profile.user_type == "DEALER":
        #    source = OrderSource(description='Buyer', value='BUYER', sort_order=1, active=True)
        #    order_sources.append(source.convert_to_dict())
        # else:
        sources = OrderSource.objects.filter(active=True).all().order_by("sort_order", "description")
        for source in sources:
            order_sources.append(source.convert_to_dict())

        return HttpResponse(json.dumps(order_sources), content_type="application/json")

    except Exception as e:
        logger.error("api_order_sources: %s" % (e))
        return HttpResponseServerError(e)


def api_order_prebook_options(request):
    pre_book_options = []
    try:
        options = DataOption.objects.filter(option_type="PRE-BOOK", active=True).all().order_by("sort_order",
                                                                                                "description")
        for option in options:
            pre_book_options.append(option.convert_to_dict())
        return HttpResponse(json.dumps(pre_book_options), content_type="application/json")

    except Exception as e:
        logger.error("api_order_sources: %s" % (e))
        return HttpResponseServerError(e)


# ------------------------------------------
#             PRODUCT ITEMS
# ------------------------------------------
def product_item_list(request, product_style_id):
    style = ProductStyle.objects.get(pk=product_style_id)
    item_list = style.product_items.filter(product_skus__active=True).distinct().order_by("item_number")

    return_list = []
    for item in item_list:
        return_list.append(item.convert_to_dict())

    return HttpResponse(json.dumps(return_list), content_type="application/json")


def product_item_grid(request, product_style_id):
    style = ProductStyle.objects.get(pk=product_style_id)
    product_items = style.product_items.all().order_by("description")

    return_list = []
    for product_item in product_items:
        skus = []
        product_skus = product_item.product_skus.filter(active=True).order_by("sku")
        for product_sku in product_skus:
            skus.append({
                "id": product_sku.pk,
                "sku": product_sku.sku,
                "item_number": product_sku.item_number,
                "style": product_sku.style,
                "description": product_sku.description,
                "size": product_sku.size,
                "upc": product_sku.upc,
                "cost": str(product_sku.cost),
                "wholesale": str(product_sku.wholesale),
                "msrp": str(product_sku.msrp),
            })

        return_list.append({
            "id": product_item.pk,
            "style_sku": style.style_sku,
            "style": style.style,
            "item_number": product_item.item_number,
            "description": product_item.description,
            "skus": skus
        })

    return HttpResponse(json.dumps(return_list), content_type="application/json")


# ------------------------------------------
#             PRODUCT SKUS
# ------------------------------------------
def product_sku_list(request, product_item_id):
    product_item = ProductItem.objects.get(pk=product_item_id)
    sku_list = product_item.product_skus.filter(active=True).distinct().order_by("sku")

    return_list = []
    for sku in sku_list:
        return_list.append(sku.convert_to_dict())

    return HttpResponse(json.dumps(return_list), content_type="application/json")


def sku_exists(sku):
    return_value = True
    try:
        sku_object = ProductSku.objects.get(sku=sku, active=True)
    except Exception as e:
        return_value = False

    return return_value


# ------------------------------------------
#             PRODUCT STYLES
# ------------------------------------------
def api_product_styles(request):
    try:
        return_object = []
        for style in ProductStyle.objects.filter(product_items__product_skus__active=True).distinct().order_by(
                "style_sku"):
            return_object.append(style.convert_to_dict())
        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_product_styles: %s" % (e))
        return HttpResponseServerError(e)


def api_product_style(request, product_style_id):
    try:
        style = ProductStyle.objects.get(pk=product_style_id)
        return_object = style.convert_to_dict()
        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_product_style: %s" % (e))
        return HttpResponseServerError(e)


def api_product_style_detail(request, product_style_id):
    try:
        return_object = product_style_detail(product_style_id)
        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_product_style_detail: %s" % (e))
        return HttpResponseServerError(e)


def product_style_detail(product_style_id):
    try:
        style = ProductStyle.objects.get(pk=product_style_id)
        product_items = style.product_items.all().order_by("item_number")

        return_object = {
            "style": style.convert_to_dict(),
            "items": [],
            "sizes": [],
        }

        sizes = []
        for product_item in product_items:
            skus = []
            high_price = 0
            low_price = 100000
            product_skus = product_item.product_skus.filter(active=True).order_by("sku")
            for product_sku in product_skus:
                size_sku = product_sku.sku[product_sku.sku.rfind("-") + 1:]
                if size_sku not in sizes:
                    sizes.append(size_sku)
                    return_object["sizes"].append({"sku": size_sku, "description": product_sku.size})

                if product_sku.wholesale > high_price:
                    high_price = product_sku.wholesale
                if product_sku.wholesale < low_price:
                    low_price = product_sku.wholesale
                skus.append(product_sku.convert_to_dict())

            if len(skus) > 0:
                product_item_dict = product_item.convert_to_dict()
                product_item_dict["skus"] = skus
                product_item_dict["sku"] = product_item_dict["itemNumber"][
                                           product_item_dict["itemNumber"].find("-") + 1:]
                product_item_dict["image"] = "%s.jpg" % product_item.item_number.replace("/", "").lower()

                if low_price == high_price:
                    product_item_dict["price"] = "$%s" % (low_price)
                else:
                    product_item_dict["price"] = "$%s-$%s" % (low_price, high_price)

                return_object["items"].append(product_item_dict)

        return_object["sizes"] = sorted(return_object["sizes"], key=lambda size: size["sku"])

        return return_object

    except Exception as e:
        logger.error("product_style_detail: %s" % (e))
        raise e


def product_style_get_id(sku):
    try:
        product_style = ProductStyle.objects.get(style_sku=sku)
        return product_style.pk
    except Exception as e:
        return 0





# ------------------------------------------
#                TERMS
# ------------------------------------------
def user_profile_terms(request):
    terms_uploaded = (request.GET.get("uploaded", "yes") == "yes")
    terms_accepted = (request.GET.get("accepted", "no") == "yes")

    return_list = []
    try:
        for user_profile in UserProfile.objects.filter(user_type="DEALER", terms_uploaded=terms_uploaded,
                                                       terms_accepted=terms_accepted).order_by("company"):
            return_list.append({
                "id": user_profile.pk,
                "rep": user_profile.account_rep.company,
                "dealer": user_profile.company,
                "terms_uploaded": user_profile.terms_uploaded,
                "terms_accepted": user_profile.terms_accepted,
                "terms_file_path": user_profile.terms_file_path.url
            })

    except Exception as e:
        logger.error("user_profile_terms: %s" % (e))

    return HttpResponse(json.dumps(return_list), content_type="application/json")


def user_profile_term(request):
    return_object = {}

    id = int(request.GET.get("id", "0"))
    try:
        user_profile = UserProfile.objects.get(pk=id)
        user_profile.terms_accepted = True
        user_profile.save()

        return_object = {
            "id": user_profile.pk,
            "rep": user_profile.account_rep.company,
            "dealer": user_profile.company,
            "terms_uploaded": user_profile.terms_uploaded,
            "terms_accepted": user_profile.terms_accepted,
            "terms_file_path": user_profile.terms_file_path.url
        }

    except Exception as e:
        logger.error("user_profile_term: %s" % (e))
        return HttpResponseServerError("Error accepting terms")

    return HttpResponse(json.dumps(return_object), content_type="application/json")


# ------------------------------------------
#            USER PROFILES
# ------------------------------------------
def api_user_profiles(request):
    try:
        return_object = []
        for user_profile in UserProfile.objects.all().order_by("company"):
            return_object.append(user_profile.convert_to_dict())
        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_user_profiles: %s" % (e))
        return HttpResponseServerError(e)


def api_user_profile(request, user_profile_id):
    try:
        user_profile = UserProfile.objects.get(pk=user_profile_id)
        return_object = user_profile.convert_to_dict()
        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_user_profile: %s" % (e))
        return HttpResponseServerError(e)


def api_user_profile_addresses(request, user_profile_id):
    try:
        return_object = []
        user_profile = UserProfile.objects.get(pk=user_profile_id)
        for user_address in UserAddress.objects.filter(user_profile=user_profile):
            return_object.append(user_address.convert_to_dict())

        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_user_profile_addresses: %s" % (e))
        return HttpResponseServerError(e)


def api_user_profile_address(request, user_profile_id, user_address_id):
    try:
        user_address = UserAddress.objects.get(pk=user_address_id)
        return_object = user_address.convert_to_dict()
        return HttpResponse(json.dumps(return_object), content_type="application/json")

    except Exception as e:
        logger.error("api_user_profile_address: %s" % (e))
        return HttpResponseServerError(e)


# ------------------------------------------
#                HELPERS
# ------------------------------------------
def valid_date(date_string):
    return_value = True
    try:
        date_object = parse(date_string)
    except Exception as e:
        logger.error("api_valid_date: %s" % (e))
        return_value = False

    return return_value


def email_submitted_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_details = []
    grand_quantity_total = 0
    grand_total = 0

    for order_detail in order.order_details.all():
        grand_quantity_total += order_detail.quantity
        grand_total += (order_detail.quantity * order_detail.price)
        order_details.append({
            "pk": order_detail.pk,
            "quantity": order_detail.quantity,
            "style": order_detail.style,
            "size": order_detail.size,
            "description": order_detail.description,
            "sku": order_detail.sku,
            "price": order_detail.price,
            "total": order_detail.quantity * order_detail.price,
        })

        data_object = {
            "image_path": settings.EMAIL_STATIC_URL,
            "order": order,
            "order_details": order_details,
            "grand_total": grand_total,
            "grand_quantity_total": grand_quantity_total,
        }

    return_value = True
    email_subject = "New Cobian Portal Order"
    email_body, email_html = make_both_emails("emails/customer_service_order_email", data_object,
                                              context_instance=RequestContext(request))

    # Send order to customer service
    return_value = send_email_safe(email_subject, email_body, settings.EMAIL_ORDERS, email_html)

    # Send emails to rep and dealer
    dealer = order.user_profile;
    rep = dealer.account_rep;
    email_list = [dealer.user.email, rep.user.email]
    return_value = send_email_safe(email_subject, email_body, email_list, email_html)

    return return_value


def order_email(request, email, order_id):
    order = Order.objects.get(pk=order_id)
    order_details = []
    grand_quantity_total = 0
    grand_total = 0

    for order_detail in order.order_details.all():
        grand_quantity_total += order_detail.quantity
        grand_total += (order_detail.quantity * order_detail.price)
        order_details.append({
            "pk": order_detail.pk,
            "quantity": order_detail.quantity,
            "style": order_detail.style,
            "size": order_detail.size,
            "description": order_detail.description,
            "sku": order_detail.sku,
            "price": order_detail.price,
            "total": order_detail.quantity * order_detail.price,
        })

        data_object = {
            "image_path": settings.EMAIL_STATIC_URL,
            "order": order,
            "order_details": order_details,
            "grand_total": grand_total,
            "grand_quantity_total": grand_quantity_total,
        }

    email_subject = "Cobian Order"
    email_body = make_html_email('emails/order_email', data_object, context_instance=RequestContext(request))

    return send_email(email_subject, email_body, email)


def email_test(request):
    return_object = {}

    return_value = send_email_safe("Test Subject", "Test Body", "brian.d.severson@gmail.com", "<h1>Test Email</h1>")

    return_object["returnValue"] = return_value

    return HttpResponse(json.dumps(return_object), content_type="application/json")
