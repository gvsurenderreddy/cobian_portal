from datetime import date
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from db.models import *

# SUDS
from suds.client import Client
from suds.transport.https import HttpAuthenticated
import lxml.etree as etree
from urllib2 import urlopen

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
logging.getLogger('suds.wsse').setLevel(logging.DEBUG)
logger = logging.getLogger("portal.db.order_factory")


def get_orders(user_profile, status, date_span, date_from, date_to, rep_orders=False):
    date_now = datetime.now()
    date_from_object = date_now
    date_to_object = date_now
    
    if date_span == "TODAY":
        date_from_object = datetime.strptime('%s/%s/%s 12:01AM' % (date_now.month, date_now.day, date_now.year), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('%s/%s/%s 11:59PM' % (date_now.month, date_now.day, date_now.year), '%m/%d/%Y %I:%M%p')
        
    if date_span == "LAST7":
        start_date = date_now - timedelta(days=7)
        date_from_object = datetime.strptime('%s/%s/%s 12:01AM' % (start_date.month, start_date.day, start_date.year), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('%s/%s/%s 11:59PM' % (date_now.month, date_now.day, date_now.year), '%m/%d/%Y %I:%M%p')
            
    if date_span == "LAST30":
        start_date = date_now - timedelta(days=30)
        date_from_object = datetime.strptime('%s/%s/%s 12:01AM' % (start_date.month, start_date.day, start_date.year), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('%s/%s/%s 11:59PM' % (date_now.month, date_now.day, date_now.year), '%m/%d/%Y %I:%M%p')

    if date_span == "LAST60":
        start_date = date_now - timedelta(days=60)
        date_from_object = datetime.strptime('%s/%s/%s 12:01AM' % (start_date.month, start_date.day, start_date.year), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('%s/%s/%s 11:59PM' % (date_now.month, date_now.day, date_now.year), '%m/%d/%Y %I:%M%p')

    if date_span == "LAST90":
        start_date = date_now - timedelta(days=90)
        date_from_object = datetime.strptime('%s/%s/%s 12:01AM' % (start_date.month, start_date.day, start_date.year), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('%s/%s/%s 11:59PM' % (date_now.month, date_now.day, date_now.year), '%m/%d/%Y %I:%M%p')
        
    if date_span == "LAST365":
        start_date = date_now - timedelta(days=365)
        date_from_object = datetime.strptime('%s/%s/%s 12:01AM' % (start_date.month, start_date.day, start_date.year), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('%s/%s/%s 11:59PM' % (date_now.month, date_now.day, date_now.year), '%m/%d/%Y %I:%M%p')
        
    if date_span == "THISMONTH":
        date_from_object = datetime.strptime('%s/1/%s 12:01AM' % (date_now.month, date_now.year), '%m/%d/%Y %I:%M%p')
        last_day = last_day_of_month(date_now)
        date_to_object = datetime.strptime('%s/%s/%s 11:59PM' % (date_now.month, last_day.day, date_now.year), '%m/%d/%Y %I:%M%p')
	
    if date_span == "LASTMONTH":
        first_day_of_this_month = datetime.strptime('%s/1/%s 12:01AM' % (date_now.month, date_now.year), '%m/%d/%Y %I:%M%p')
        last_month = first_day_of_this_month - timedelta(days=1)
        date_from_object = datetime.strptime('%s/1/%s 12:01AM' % (last_month.month, last_month.year), '%m/%d/%Y %I:%M%p')
        last_day = last_day_of_month(date_from_object)
        date_to_object = datetime.strptime('%s/%s/%s 11:59PM' % (last_month.month, last_day.day, last_month.year), '%m/%d/%Y %I:%M%p')
    
    if date_span == "THISYEAR":
        date_from_object = datetime.strptime('1/1/%s 12:01AM' % (date_now.year), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('12/31/%s 12:01AM' % (date_now.year), '%m/%d/%Y %I:%M%p')

    if date_span == "LASTYEAR":
        date_from_object = datetime.strptime('1/1/%s 12:01AM' % (date_now.year - 1), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('12/31/%s 11:59PM' % (date_now.year - 1), '%m/%d/%Y %I:%M%p')

    if date_span == "CUSTOM":
        date_from_object = datetime.strptime('%s 12:01AM' % (date_from), '%m/%d/%Y %I:%M%p')
        date_to_object = datetime.strptime('%s 11:59PM' % (date_to), '%m/%d/%Y %I:%M%p')
    
    if rep_orders:
        if user_profile.user_type == "CUSTOMER_SERVICE":
            # user_profile is customer service...
            orders = Order.objects.filter(status=status, status_date__range=[date_from_object, date_to_object]).order_by("user_profile__company", "-status_date")
        else:
            # user_profile is the rep...
            orders = Order.objects.filter(user_profile__account_rep=user_profile, status=status, status_date__range=[date_from_object, date_to_object]).order_by("user_profile__company", "-status_date")
    else:
        # user_profile is the dealer...
        orders = Order.objects.filter(user_profile=user_profile, status=status, status_date__range=[date_from_object, date_to_object]).order_by("-status_date")
    
    order_array = []
    grand_total = 0
    for order in orders:
        total = 0
        for order_detail in order.order_details.all():
            total += order_detail.quantity * order_detail.price
        grand_total += total
        
        order_status = "NEW"
        for value, description in Order.ORDER_STATUS:
            if value == order.status:
                order_status = description
                continue
        
        order_array.append({
                "order_number": order.pk,
                "po_number": order.po_number,
                "dealer_id": order.user_profile.pk,
                "dealer": order.user_profile.company,
                "order_date": order.order_date,
                "status_date": order.status_date,
                "status": order_status,
                "total": total,
            })
            
    return {
        "order_array": order_array,
        "grand_total": grand_total
        }
    
def send_order(order_number):
    returnValue = True

    try:
        order = Order.objects.get(pk=order_number)
        notes_stripped = None
        if order.notes:
            notes_stripped = order.notes.replace("\n", " ")
            notes_stripped = notes_stripped.replace("\r", " ")
        
        if order:
            dateNow = datetime.now()

            orderUrl = "%s%s" % (settings.ORDER_URL, "xml/order.xml")
            orderDoc = etree.parse(orderUrl).getroot()

            po_number = "%s-%s" % (order.user_profile.account_id, order.pk)
            if order.po_number:
                po_number = order.po_number.replace("&", "&amp;")
                
            orderDoc[0][0][0].text = po_number
            orderDoc[0][1].text = "%sT00:00:01" % (dateNow.strftime("%Y-%m-%d"))
            if order.order_type == "AT-ONCE":
                orderDoc[0][8][0].text = "%sT00:00:01" % (order.prebook_date.strftime("%Y-%m-%d"))
                orderDoc[0][8][1].text = "%sT00:00:01" % (order.prebook_date.strftime("%Y-%m-%d"))
                orderDoc[0][8][2].text = "%sT00:00:01" % (order.prebook_date.strftime("%Y-%m-%d"))
                orderDoc[0][8][4].text = "%sT00:00:01" % (order.cancel_date.strftime("%Y-%m-%d"))
            else:
                pre_book_date = get_pre_book_date(order)
                orderDoc[0][8][0].text = pre_book_date
                orderDoc[0][8][1].text = pre_book_date
                orderDoc[0][8][2].text = pre_book_date
                
            #orderDoc[0][9][0][0][0].text = order.user_profile.account_id
            orderDoc[0][9][2][0][0].text = order.user_profile.account_id
            orderDoc[0][9][2][1][0][0].text = order.user_profile.account_id

            orderDoc[0][9][2][2][0].text = order.shipto_name.replace("&", "&amp;")
            orderDoc[0][9][2][2][1].text = order.shipto_address_id.replace("&", "&amp;")

            if order.shipto_address2:
                orderDoc[0][9][2][2][2].text = "%s %s" % (order.shipto_address1.replace("&", "&amp;"), order.shipto_address2.replace("&", "&amp;"))
            else:
                orderDoc[0][9][2][2][2].text = "%s" % (order.shipto_address1.replace("&", "&amp;"))
                
            orderDoc[0][9][2][2][3].text = order.shipto_postal_code
            orderDoc[0][9][2][2][4].text = order.shipto_city.replace("&", "&amp;")
            orderDoc[0][9][2][2][5][1].text = order.shipto_state.replace("&", "&amp;")
            if order.shipto_country:
                orderDoc[0][9][2][2][6][0].text = order.shipto_country.replace("&", "&amp;")


            orderDoc[0][9][3][0][0].text = order.user_profile.account_id.replace("&", "&amp;")
            orderDoc[0][9][3][1][0][0].text = order.user_profile.account_id.replace("&", "&amp;")

            orderDoc[0][9][3][2][0].text = order.billto_name.replace("&", "&amp;")
            
            if order.billto_address2:
                orderDoc[0][9][3][2][1].text = "%s %s" % (order.billto_address1.replace("&", "&amp;"), order.billto_address2.replace("&", "&amp;"))
            else:
                orderDoc[0][9][3][2][1].text = "%s" % (order.billto_address1.replace("&", "&amp;"))
                
            orderDoc[0][9][3][2][2].text = order.billto_postal_code.replace("&", "&amp;")
            orderDoc[0][9][3][2][3].text = order.billto_city.replace("&", "&amp;")
            orderDoc[0][9][3][2][4][1].text = order.billto_state.replace("&", "&amp;")
            if order.billto_country:
                orderDoc[0][9][3][2][5][0].text = order.billto_country.replace("&", "&amp;")
            #orderDoc[0][11][0][0].text = "Processing"
            
            # Add order source in the notes field
            if notes_stripped:
                notes_stripped = "%s - Order Source: %s" % (notes_stripped, order.order_source)
            else:
                notes_stripped = "Order Source: %s" % (order.order_source)

            orderDoc[0][12][0][1][0][1].text = notes_stripped.replace("&", "&amp;")

            line_item_number = 0
            for orderDetail in order.order_details.all():
                line_item_number += 1
                ItemDetail = etree.SubElement(orderDoc[1][0], "ItemDetail")
                BaseItemDetail = etree.SubElement(ItemDetail, "BaseItemDetail")
                LineItemNum = etree.SubElement(BaseItemDetail, "LineItemNum")
                etree.SubElement(LineItemNum, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}BuyerLineItemNum").text = str(line_item_number)
                ItemIdentifiers = etree.SubElement(BaseItemDetail, "ItemIdentifiers")
                PartNumbers = etree.SubElement(ItemIdentifiers, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}PartNumbers")
                SellerPartNumber = etree.SubElement(PartNumbers, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}SellerPartNumber")
                etree.SubElement(SellerPartNumber, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}PartID").text = orderDetail.sku
                TotalQuantity = etree.SubElement(BaseItemDetail, "TotalQuantity")
                etree.SubElement(TotalQuantity, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}QuantityValue").text = str(orderDetail.quantity)
                UnitOfMeasurement = etree.SubElement(TotalQuantity, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}UnitOfMeasurement")
                etree.SubElement(UnitOfMeasurement, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}UOMCoded").text = "Other"
                etree.SubElement(UnitOfMeasurement, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}UOMCodedOther").text = "EA"
                PricingDetail = etree.SubElement(ItemDetail, "PricingDetail")
                ListOfPrice = etree.SubElement(PricingDetail, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}ListOfPrice")
                Price = etree.SubElement(ListOfPrice, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}Price")
                UnitPrice = etree.SubElement(Price, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}UnitPrice")
                etree.SubElement(UnitPrice, "{rrn:org.xcbl:schemas/xcbl/v4_0/core/core.xsd}UnitPriceValue").text = str(orderDetail.price)

            xmlData = etree.tostring(orderDoc, pretty_print=True)
            
            dateNow = datetime.now()
            fileName = "ORDER%s-%s" % (dateNow.strftime("%Y%m%d%I%M"), order_number)

            if settings.ENVIRONMENT == "LOCAL":
                returnValue = True
            else:
                client = Client(settings.EBRIDGE_WSDL, location=settings.EBRIDGE_URL)
                returnValue = client.service.SendFile(settings.EBRIDGE_LOGIN, settings.EBRIDGE_PASSWORD, xmlData, fileName)
        else:
            logger.error("Failed to send order #%s to ebridge: Invalid Order!", order_number)
            returnValue = False

    except Exception as e:
        logger.error("Failed to send order #%s to ebridge: %s", order_number, e)
        returnValue = False

    return returnValue
    
def get_pre_book_date(order):
    dateNow = datetime.now()
    return_date = "%sT00:00:01" % (dateNow.strftime("%Y-%m-%d"))
    
    # Get first pre-book option as default date
    try:
        option = DataOption.objects.filter(option_type="PRE-BOOK", active=True).all().order_by("sort_order", "description")[0]
        date_object = datetime.strptime('%s 12:01AM' % (option.value), '%m/%d/%Y %I:%M%p')
        return_date = "%sT00:00:01" % (date_object.strftime("%Y-%m-%d"))
    except Exception as e:
        pass
        
    try:
        date_object = datetime.strptime('%s 12:01AM' % (order.pre_book_option), '%m/%d/%Y %I:%M%p')
        return_date = "%sT00:00:01" % (date_object.strftime("%Y-%m-%d"))
    except Exception as e:
        pass
    
    return return_date
    
def get_default_data_option(option_type):
    option = None

    # Get first pre-book option as default date
    try:
        option = DataOption.objects.filter(option_type=option_type, active=True).all().order_by("sort_order", "description")[0]
    except Exception as e:
        pass

    return option.value
        
def last_day_of_month(dt):
    return date(dt.year, dt.month, 1).replace(day=1,month=date(dt.year,dt.month,1).month+1)-timedelta(days=1)

def first_day_of_month(dt):
    return datetime.date(day=1, month=dt.month, year=dt.year)
    