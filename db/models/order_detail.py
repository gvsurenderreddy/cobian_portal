from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
     
class OrderDetail(models.Model):
    order = models.ForeignKey("Order", verbose_name=_("Order"), related_name='order_details', blank=True, null=True)
    quantity = models.IntegerField(_("Quantity"), default=1, blank=True)
    sku = models.CharField(_("Sku"), max_length=50, blank=True)
    item_number = models.CharField(_("Item Number"), max_length=50, blank=True)
    style = models.CharField(_("Style"), max_length=50, blank=True)
    description = models.CharField(_("Description"), max_length=50, blank=True)
    size = models.CharField(_("Size"), max_length=50, blank=True)
    upc = models.CharField(_("UPC"), max_length=50, blank=True)
    cost = models.DecimalField(_("Cost"), max_digits=7, decimal_places=2, default=0, blank=False)
    price = models.DecimalField(_("Price"), max_digits=7, decimal_places=2, default=0, blank=False)

    def __str__(self):
        return "%s - %s %s" % (self.sku, self.style, self.description)
    
    def convert_to_dict(self):
        return {
            "id": self.pk,
            "orderId": self.order.pk,
            "quantity": self.quantity,
            "sku": self.sku,
            "itemNumber": self.item_number,
            "style": self.style,
            "description": self.description,
            "size": self.size,
            "upc": self.upc,
            "cost": self.cost,
            "price": self.price,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"
        ordering = ["sku"]