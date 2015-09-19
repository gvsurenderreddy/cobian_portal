from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
from datetime import datetime
     
class Order(models.Model):
    ORDER_STATUS = (
        ("NEW", "New Order"),
        ("SUBMIT", "Submitted"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
    )
    ORDER_TYPE = (
        ("AT-ONCE", "At Once"),
        ("PRE-BOOK", "Pre-Book"),
        ("PROPOSE", "Proposed"),
    )
    
    user_profile = models.ForeignKey("UserProfile", related_name='orders', blank=True, null=True)
    order_source = models.CharField(_("Order Source"), max_length=50, blank=True, null=True, default="")
    in_house_sales = models.CharField(_("In House Sales"), max_length=50, blank=True, null=True, default="")
    po_number = models.CharField(_("PO Number"), max_length=50, blank=True, null=True, default="")
    status = models.CharField(default="NEW", choices=ORDER_STATUS, max_length=20)
    order_type = models.CharField(default="AT-ONCE", choices=ORDER_TYPE, max_length=20)
    status_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(auto_now_add=True)
    prebook_date = models.DateTimeField(blank=True, null=True)
    cancel_date = models.DateTimeField(blank=True, null=True)
    pre_book_option = models.CharField(_("Pre-Book Option"), max_length=100, blank=True, null=True)
    notes = models.TextField(_("Notes"), blank=True, null=True)
    billto_name = models.CharField(_("Bill To Name"), max_length=100, blank=True)
    billto_address1 = models.CharField(_("Bill To Address"),max_length=50, blank=True, null=True)
    billto_address2 = models.CharField(_("Bill To Address"), max_length=50, blank=True, null=True)
    billto_city = models.CharField(_("Bill To City"), max_length=50, blank=True, null=True)
    billto_state = models.CharField(_("Bill To State"), max_length=30, blank=True, null=True)
    billto_postal_code = models.CharField(_("Bill To Zip Code"), blank=True, null=True, max_length=9)
    billto_country = models.CharField(_("Bill To Country"), blank=True, null=True, max_length=50)
    billto_phone = models.CharField(_("Bill To Phone Number"), blank=True, null=True, max_length=30)
    billto_email = models.CharField(_("Bill To Email"), blank=True, null=True, max_length=100)
    shipto_name = models.CharField(_("Ship To Name"), max_length=100, blank=True)
    shipto_address_id = models.CharField(_("Ship To Address ID"), max_length=200, blank=True, null=True)
    shipto_address1 = models.CharField(_("Ship To Address"),max_length=50, blank=True, null=True)
    shipto_address2 = models.CharField(_("Ship To Address"), max_length=50, blank=True, null=True)
    shipto_city = models.CharField(_("Ship To City"), max_length=50, blank=True, null=True)
    shipto_state = models.CharField(_("Ship To State"), max_length=30, blank=True, null=True)
    shipto_postal_code = models.CharField(_("Ship To Zip Code"), blank=True, null=True, max_length=9)
    shipto_country = models.CharField(_("Ship To Country"), blank=True, null=True, max_length=50)
    shipto_phone = models.CharField(_("Ship To Phone Number"), blank=True, null=True, max_length=30)
    shipto_email = models.CharField(_("Ship To Email"), blank=True, null=True, max_length=100)
    
    def __str__(self):
        return "%s - %s %s" % (self.pk, self.shipto_name, self.order_date)
        
    def convert_to_dict(self):
        return {
            "id": self.pk,
            "dealerId": self.user_profile.pk,
            "orderSource": self.order_source,
            "inHouseSales": self.in_house_sales,
            "poNumber": self.po_number,
            "status": self.status,
            "orderType": self.order_type,
            "statusDate": self.status_date.strftime('%m/%d/%Y'),
            "orderDate": self.order_date.strftime('%m/%d/%Y'),
            "prebookDate": self.prebook_date.strftime('%m/%d/%Y'),
            "cancelDate": self.cancel_date.strftime('%m/%d/%Y'),
            "prebookOption": self.pre_book_option,
            "notes": self.notes,
            "billtoName": self.billto_name,
            "billtoAddress1": self.billto_address1,
            "billtoAddress2": self.billto_address2,
            "billtoCity": self.billto_city,
            "billtoState": self.billto_state,
            "billtoPostalCode": self.billto_postal_code,
            "billtoCountry": self.billto_country,
            "billtoPhone": self.billto_phone,
            "billtoEmail": self.billto_email,
            "shiptoName": self.shipto_name,
            "shiptoAddressId": self.shipto_address_id,
            "shiptoAddress1": self.shipto_address1,
            "shiptoAddress2": self.shipto_address2,
            "shiptoCity": self.shipto_city,
            "shiptoState": self.shipto_state,
            "shiptoPostalCode": self.shipto_postal_code,
            "shiptoCountry": self.shipto_country,
            "shiptoPhone": self.shipto_phone,
            "shiptoEmail": self.shipto_email,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["order_date"]