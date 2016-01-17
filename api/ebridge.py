# DJANGO
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from datetime import datetime
from decimal import *

# JSON
import ujson as json

# SUDS
from suds.client import Client
import lxml.etree as etree
import logging

# MODELS
from db.models.user_profile import User, UserProfile
from db.models.product_sku import ProductSku
from db.models.product_item import ProductItem
from db.models.product_style import ProductStyle

logger = logging.getLogger("api.ebridge")


def ebridge_documents(request):
    return_list = []
    date_now = datetime.now()
    from_date = datetime.strptime('1/1/{} 12:01AM'.format(date_now.year), '%m/%d/%Y %I:%M%p')
    to_date = date_now

    logger.error("ebridge_document: TEST LOGGER")

    doc_type = request.GET.get("type", "INVRPT")
    status = request.GET.get("status", "New")
    if status == "Range":
        status = "All"
        try:
            start_date = datetime.strptime(request.GET.get("start"), '%Y-%m-%d')
            from_date = datetime.strptime("{}/{}/{} 12:01AM".format(start_date.month, start_date.day, start_date.year),
                                          '%m/%d/%Y %I:%M%p')

            end_date = datetime.strptime(request.GET.get("end"), '%Y-%m-%d')
            to_date = datetime.strptime('{}/{}/{} 11:59PM'.format(end_date.month, end_date.day, end_date.year),
                                        '%m/%d/%Y %I:%M%p')
        except Exception as e:
            from_date = datetime.strptime('{}/{}/{} 12:01AM'.format(date_now.month, date_now.day, date_now.year),
                                          '%m/%d/%Y %I:%M%p')
            to_date = datetime.strptime('{}/{}/{} 11:59PM'.format(date_now.month, date_now.day, date_now.year),
                                        '%m/%d/%Y %I:%M%p')

    try:
        client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)

        return_value = client.service.GetDocumentList2(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, status,
                                                       doc_type, settings.EBRIDGE_PARTNER, from_date, to_date)

        doc = etree.fromstring(return_value)

        if len(doc) > 1:
            documentList = doc[1]

            return_list.append({
                "doc_num": documentList.get("doc_num"),
                "doc_sys_no": documentList.get("doc_sys_no"),
                "tran_datetime": documentList.get("tran_datetime"),
                "doc_date": documentList.get("doc_date"),
                "flag": 0
            })
            for document in documentList:
                return_list.append({
                    "doc_num": document.get("doc_num"),
                    "doc_sys_no": document.get("doc_sys_no"),
                    "tran_datetime": document.get("tran_datetime"),
                    "doc_date": document.get("doc_date"),
                    "flag": 0
                })
    except Exception as e:
        logger.error("ebridge_documents: {}".format(e))

    return HttpResponse(json.dumps(return_list), content_type="application/json")


def ebridge_document(request):
    doc_type = request.GET.get("doc_type", None)
    doc_sys_no = request.GET.get("doc_sys_no", None)

    if doc_type and doc_sys_no:
        document = {}
        return_value = "Invalid doc_type"
        if doc_type == "INVRPT":
            document = get_document_product(doc_sys_no)
            return_value = import_document_product(document)

        if doc_type == "PARTIN":
            document = get_document_partner(doc_sys_no)
            return_value = import_document_partner(document)

        if return_value == "Success":
            return HttpResponse(json.dumps(document), content_type="application/json")
        else:
            logger.error("ebridge_document: {}".format(return_value))
            return HttpResponseServerError(return_value)
    else:
        logger.error("ebridge_document: No doc_type and/or doc_sys_no provided!")
        return HttpResponseServerError("No doc_type and/or doc_sys_no provided!")


def get_document_list(doc_type, status="New", date_range="year"):
    return_list = []
    date_now = datetime.now()
    from_date = datetime.strptime('1/1/%s 12:01AM' % (date_now.year), '%m/%d/%Y %I:%M%p')
    if date_range == "today":
        from_date = datetime.strptime('%s/%s/%s 12:01AM' % (date_now.month, date_now.day, date_now.year),
                                     '%m/%d/%Y %I:%M%p')
    if date_range == "yesterday":
        from_date = datetime.strptime('%s/%s/%s 12:01AM' % (date_now.month, date_now.day - 1, date_now.year),
                                     '%m/%d/%Y %I:%M%p')
    if date_range == "month":
        from_date = datetime.strptime('%s/1/%s 12:01AM' % (date_now.month, date_now.year), '%m/%d/%Y %I:%M%p')
    to_date = date_now

    try:
        client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)

        return_value = client.service.GetDocumentList2(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, status,
                                                      doc_type, settings.EBRIDGE_PARTNER, from_date, to_date)

        doc = etree.fromstring(return_value)

        if len(doc) > 1:
            documentList = doc[1]

            return_list.append({
                "doc_num": documentList.get("doc_num"),
                "doc_sys_no": documentList.get("doc_sys_no"),
                "tran_datetime": documentList.get("tran_datetime"),
                "doc_date": documentList.get("doc_date")
            })
            for document in documentList:
                return_list.append({
                    "doc_num": document.get("doc_num"),
                    "doc_sys_no": document.get("doc_sys_no"),
                    "tran_datetime": document.get("tran_datetime"),
                    "doc_date": document.get("doc_date")
                })
    except Exception as e:
        logger.error("get_document_list: {}".format(e))

    return return_list


def get_document_product(doc_sys_no):
    return_object = {}

    try:
        client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)

        return_value = client.service.GetDocument(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, doc_sys_no)

        return_value = strip_xml_declaration(return_value)

        my_xml = etree.XML(return_value)

        if return_value:
            documents = etree.XML(return_value)

            catalogData = documents[3]

            productId = None
            productName = ""
            description = ""
            price = 0
            costPrice = 0
            retailPrice = 0
            inventory = 0

            for catalogElement in catalogData:
                # Product info
                if catalogElement.tag.lower().endswith("product"):
                    for productElement in catalogElement:
                        if productElement.tag.lower().endswith("productid"):
                            productId = productElement.text
                        if productElement.tag.lower().endswith("productname"):
                            productName = productElement.text
                        if productElement.tag.lower().endswith("longdescription"):
                            description = productElement.text

                # Pricing info
                if catalogElement.tag.lower().endswith("pricing"):
                    for pricingElement in catalogElement:
                        if pricingElement.tag.lower().endswith("productcostprice"):
                            costPrice = pricingElement[0].text
                        if pricingElement.tag.lower().endswith("productprice"):
                            price = pricingElement[0].text
                        if pricingElement.tag.lower().endswith("retail_price"):
                            retailPrice = pricingElement[0].text

                # Inventory info
                if catalogElement.tag.lower().endswith("inventoryreportdetail"):
                    for inventoryElement in catalogElement:
                        if inventoryElement.tag.lower().endswith("totalinventoryquantity"):
                            for quantityElement in inventoryElement:
                                if quantityElement.tag.lower().endswith("quantityvalue"):
                                    inventory = quantityElement.text

            return_object = {
                "product_id": productId,
                "product_name": productName,
                "description": description,
                "price": price,
                "cost_price": costPrice,
                "retail_price": retailPrice,
                "inventory": inventory,
            }

    except Exception as e:
        logger.error("get_document_product: {}".format(e))

    return return_object


def import_document_product(document_product):
    return_value = "Success"

    sku = document_product["product_id"]
    inventory = int(document_product["inventory"])
    cost = Decimal(document_product["cost_price"])
    wholesale = Decimal(document_product["price"])
    msrp = Decimal(document_product["retail_price"])
    active = True

    if sku:
        try:
            product_sku = ProductSku.objects.get(sku=sku)
            product_sku.inventory = inventory
            product_sku.cost = cost
            product_sku.wholesale = wholesale
            product_sku.msrp = msrp
            product_sku.active = active
            product_sku.save()

        except ProductSku.DoesNotExist:
            try:
                sku_array = sku.split("-")
                name_array = document_product["product_name"].split("-")
                style_sku = sku_array[0]
                style = name_array[0].strip()
                item_number = "%s-%s" % (sku_array[0], sku_array[1])

                if len(name_array) > 1:
                    description = name_array[1].strip()
                else:
                    description = ""

                if len(name_array) > 2:
                    size = name_array[2].strip()
                else:
                    size = ""

                # Create ProductStyle...
                try:
                    product_style = ProductStyle.objects.get(style_sku=style_sku)
                except ProductStyle.DoesNotExist:
                    product_style = ProductStyle(style_sku=style_sku, style=style)
                    product_style.save()

                # Create ProductItem...
                try:
                    product_item = ProductItem.objects.get(product_style=product_style, item_number=item_number)
                except ProductItem.DoesNotExist:
                    product_item = ProductItem(product_style=product_style, item_number=item_number,
                                               description=description, available=datetime.now())
                    product_item.save()

                product_sku = ProductSku(product_item=product_item, sku=sku, item_number=item_number, style=style,
                                         description=description, size=size, inventory=inventory, cost=cost,
                                         wholesale=wholesale, msrp=msrp, active=active)
                product_sku.save()

            except Exception as e:
                logger.error("import_document_product: {}".format(e))
                return_value = "Error parsing sku %s: %s" % (sku, e)

        except Exception as e:
            logger.error("import_document_product: {}".format(e))
            return_value = "Error importing %s : %s (%s)" % (sku, e, type(e))
    else:
        return_value = "Invalid Sku"

    return return_value


def get_document_partner(doc_sys_no):
    return_object = {}

    try:
        client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)

        return_value = client.service.GetDocument(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, doc_sys_no)
        return_value = strip_xml_declaration(return_value)
        my_xml = etree.XML(return_value)

        if return_value:
            documents = etree.XML(return_value)

            # Initialize...
            name = None
            account_id = None
            rep_id = None
            shipTo = []
            billToName = None
            billToStreet = None
            billToCity = None
            billToPostalCode = None
            billToRegion = None
            billToCountry = None

            for document in documents:
                if document.tag.lower().endswith("billtoparty"):
                    billToParty = document
                    for billToElement in billToParty:
                        if billToElement.tag.lower().endswith("partyid"):
                            account_id = billToElement[0].text

                        if billToElement.tag.lower().endswith("nameaddress"):
                            for nameAddressElement in billToElement:
                                if nameAddressElement.tag.lower().endswith("name1"):
                                    billToName = nameAddressElement.text
                                if nameAddressElement.tag.lower().endswith("street"):
                                    billToStreet = nameAddressElement.text
                                if nameAddressElement.tag.lower().endswith("postalcode"):
                                    billToPostalCode = nameAddressElement.text
                                if nameAddressElement.tag.lower().endswith("city"):
                                    billToCity = nameAddressElement.text
                                if nameAddressElement.tag.lower().endswith("region"):
                                    for regionElement in nameAddressElement:
                                        if regionElement.tag.lower().endswith("regioncodedother"):
                                            billToRegion = regionElement.text
                                if nameAddressElement.tag.lower().endswith("country"):
                                    for countryElement in nameAddressElement:
                                        if countryElement.tag.lower().endswith("countrycodedother"):
                                            billToCountry = countryElement.text

                if document.tag.lower().endswith("shiptoparty"):
                    shipToParty = document
                    shipToName = None
                    shipToAddressId = None
                    shipToStreet = None
                    shipToCity = None
                    shipToPostalCode = None
                    shipToRegion = None
                    shipToCountry = None

                    for shipToElement in shipToParty:
                        if shipToElement.tag.lower().endswith("nameaddress"):
                            for nameAddressElement in shipToElement:
                                if nameAddressElement.tag.lower().endswith("name1"):
                                    shipToName = nameAddressElement.text
                                if nameAddressElement.tag.lower().endswith("street"):
                                    shipToStreet = nameAddressElement.text
                                if nameAddressElement.tag.lower().endswith("postalcode"):
                                    shipToPostalCode = nameAddressElement.text
                                if nameAddressElement.tag.lower().endswith("city"):
                                    shipToCity = nameAddressElement.text
                                if nameAddressElement.tag.lower().endswith("region"):
                                    for regionElement in nameAddressElement:
                                        if regionElement.tag.lower().endswith("regioncodedother"):
                                            shipToRegion = regionElement.text
                                if nameAddressElement.tag.lower().endswith("country"):
                                    for countryElement in nameAddressElement:
                                        if countryElement.tag.lower().endswith("countrycodedother"):
                                            shipToCountry = countryElement.text

                        if shipToElement.tag.lower().endswith("primarycontact"):
                            for primaryContactElement in shipToElement:
                                if primaryContactElement.tag.lower().endswith("listofcontactnumber"):
                                    for listOfContactNumberElement in primaryContactElement:
                                        if listOfContactNumberElement.tag.lower().endswith("contactnumber"):
                                            for contactNumberElement in listOfContactNumberElement:
                                                if contactNumberElement.tag.lower().endswith("contactnumbervalue"):
                                                    shipToAddressId = contactNumberElement.text

                    shipTo.append({
                        "shipToName": shipToName,
                        "shipToAddressId": shipToAddressId,
                        "shipToStreet": shipToStreet,
                        "shipToCity": shipToCity,
                        "shipToPostalCode": shipToPostalCode,
                        "shipToRegion": shipToRegion,
                        "shipToCountry": shipToCountry,
                    })

                if document.tag.lower().endswith("listofnamevalueset"):
                    nameValues = document
                    for nameValuePair in nameValues[0][1]:
                        if nameValuePair[0].text.lower() == "dealer":
                            name = nameValuePair[1].text
                        if nameValuePair[0].text.lower() == "salesemployee":
                            rep_id = nameValuePair[1].text

            return_object = {
                "name": name,
                "account_id": account_id,
                "rep_id": rep_id,
                "shipTo": shipTo,
                "billToName": billToName,
                "billToStreet": billToStreet,
                "billToCity": billToCity,
                "billToPostalCode": billToPostalCode,
                "billToRegion": billToRegion,
                "billToCountry": billToCountry,
            }

    except Exception as e:
        logger.error("get_document_partner: {}".format(e))

    return return_object


def import_document_partner(document_partner):
    return_value = "Success"
    try:
        # First, lets get the rep for this partner, if there is no rep, do not import...
        rep_user_profile = UserProfile.objects.get(account_id=document_partner["rep_id"])

        # Now lets import the partner...
        create_partner = False
        partner_exists = False
        try:
            user = User.objects.get(username=document_partner["account_id"])
            user_profile = UserProfile.objects.get(user=user)
            user_profile.account_rep = rep_user_profile
            user_profile.company = document_partner["name"][:100]
            user_profile.save()

            partner_exists = True

        except Exception as e:
            create_partner = True

        if create_partner:
            if document_partner["account_id"] and document_partner["name"]:
                try:
                    user = User(username=document_partner["account_id"][:30], is_staff=False, is_active=True,
                                is_superuser=False)
                    user.set_password(document_partner["account_id"][:30])
                    user.first_name = document_partner["name"][:30]
                    user.save()

                    user_profile = UserProfile(user=user, user_type="DEALER",
                                               account_id=document_partner["account_id"][:50],
                                               account_rep=rep_user_profile, company=document_partner["name"][:100])
                    user_profile.save()
                    partner_exists = True

                except Exception as e:
                    return_value = "Import partner (%s) : %s" % (document_partner["account_id"], e)
            else:
                return_value = "No account_id or name"

        if partner_exists:
            # First, lets delete all existing addresses for this partner.
            try:
                address_list = UserAddress.objects.filter(user_profile=user_profile).all()
                for address in address_list:
                    address.delete()

            except Exception as e:
                pass

            # Import BillTo address...
            if document_partner["billToName"] and document_partner["billToStreet"] and document_partner[
                "billToCity"] and document_partner["billToRegion"] and document_partner["billToPostalCode"] and \
                    document_partner["billToCountry"]:
                try:
                    user_address = UserAddress(user_profile=user_profile, address_type="BILLTO",
                                               name=document_partner["billToName"][:200],
                                               address1=document_partner["billToStreet"][:50],
                                               city=document_partner["billToCity"][:30],
                                               state=document_partner["billToRegion"][:30],
                                               postal_code=document_partner["billToPostalCode"][:9],
                                               country=document_partner["billToCountry"][:30])
                    user_address.save()
                except Exception as e:
                    pass

            # Import ShipTo addresses...
            for ship_to in document_partner["shipTo"]:
                if ship_to["shipToName"] and ship_to["shipToAddressId"] and ship_to["shipToStreet"] \
                        and ship_to["shipToCity"] and ship_to["shipToRegion"] and ship_to["shipToPostalCode"] \
                        and ship_to["shipToCountry"]:
                    # First see if it exists so we don't import duplicate addresses
                    try:
                        user_address = UserAddress.objects.get(user_profile=user_profile, address_type="SHIPTO",
                                                               address_id=ship_to["shipToAddressId"][:200])
                    except Exception as e:
                        try:
                            user_address = UserAddress(user_profile=user_profile, address_type="SHIPTO",
                                                       name=ship_to["shipToName"][:200],
                                                       address_id=ship_to["shipToAddressId"][:200],
                                                       address1=ship_to["shipToStreet"][:50],
                                                       city=ship_to["shipToCity"][:30],
                                                       state=ship_to["shipToRegion"][:30],
                                                       postal_code=ship_to["shipToPostalCode"][:9],
                                                       country=ship_to["shipToCountry"][:30])
                            user_address.save()
                        except Exception as e:
                            pass

    except Exception as e:
        return_value = "Rep not found (%s) : %s" % (document_partner["rep_id"], e)

    return return_value


def delete_document_list(doc_sys_list):
    return_flag = True
    try:
        client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)

        return_value = client.service.DeleteDocuments(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, doc_sys_list)
        if isinstance(return_value, unicode):
            return_value = return_value.encode("utf-8")

    except Exception as e:
        logger.error("delete_document_list: {}".format(e))
        return_flag = False

    return return_flag


def get_document_list_json(request, doc_type):
    return_list = []
    status = "All"
    date_now = datetime.now()
    from_date = datetime.strptime('1/1/%s 12:01AM' % (date_now.year), '%m/%d/%Y %I:%M%p')
    to_date = date_now

    client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)

    return_value = client.service.GetDocumentList2(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, status, doc_type,
                                                  settings.EBRIDGE_PARTNER, from_date, to_date)

    if isinstance(return_value, unicode):
        return_value = return_value.encode("utf-8")

    doc = etree.fromstring(return_value)

    if len(doc) > 1:
        documentList = doc[1]

        return_list.append({
            "doc_num": documentList.get("doc_num"),
            "doc_sys_no": documentList.get("doc_sys_no"),
            "tran_datetime": documentList.get("tran_datetime"),
            "doc_date": documentList.get("doc_date")
        })
        for document in documentList:
            return_list.append({
                "doc_num": document.get("doc_num"),
                "doc_sys_no": document.get("doc_sys_no"),
                "tran_datetime": document.get("tran_datetime"),
                "doc_date": document.get("doc_date")
            })

    return HttpResponse(json.dumps(return_list), content_type="application/json")


def get_document(request, doc_type, doc_sys_no):
    if doc_type.lower() == "prodat":
        return get_product(request, doc_sys_no)

    if doc_type.lower() == "850":
        return get_order(request, doc_sys_no)


def get_order(request, doc_sys_no):
    client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)

    return_value = client.service.GetDocument(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, doc_sys_no)
    return_value = strip_xml_declaration(return_value)

    return HttpResponse(return_value, content_type="application/xml")


def get_product(request, doc_sys_no):
    return_object = {}

    client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)

    return_value = client.service.GetDocument(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, doc_sys_no)
    return_value = strip_xml_declaration(return_value)
    my_xml = etree.XML(return_value)

    if return_value:
        documents = etree.XML(return_value)

        catalogData = documents[4]

        productId = None
        productName = None
        description = None
        price = 0
        costPrice = 0
        retailPrice = 0
        inventory = 0

        for catalogElement in catalogData:
            # Product info
            if catalogElement.tag.lower().endswith("product"):
                for productElement in catalogElement:
                    if productElement.tag.lower().endswith("productid"):
                        productId = productElement.text
                    if productElement.tag.lower().endswith("productname"):
                        productName = productElement.text
                    if productElement.tag.lower().endswith("longdescription"):
                        description = productElement.text

            # Pricing info
            if catalogElement.tag.lower().endswith("pricing"):
                for pricingElement in catalogElement:
                    if pricingElement[1].text.lower().endswith("cost_price"):
                        costPrice = pricingElement[0].text
                    if pricingElement[1].text.lower().endswith("price"):
                        price = pricingElement[0].text
                    if pricingElement[1].text.lower().endswith("retail_price"):
                        retailPrice = pricingElement[0].text

            # Inventory info
            if catalogElement.tag.lower().endswith("inventoryreportdetail"):
                for inventoryElement in catalogElement:
                    if inventoryElement.tag.lower().endswith("totalinventoryquantity"):
                        for quantityElement in inventoryElement:
                            if quantityElement.tag.lower().endswith("quantityvalue"):
                                inventory = quantityElement.text

        return_object = {
            "product_id": productId,
            "product_name": productName,
            "description": description,
            "price": price,
            "cost_price": costPrice,
            "retail_price": retailPrice,
            "inventory": inventory,
        }

    return HttpResponse(json.dumps(return_object), content_type="application/json")


def strip_xml_declaration(xml_string):
    xml_start = xml_string.index("<?xml")
    xml_end = xml_string.index("?>")
    if xml_end > xml_start:
        return xml_string[xml_end+2:]
    else:
        return xml_string
