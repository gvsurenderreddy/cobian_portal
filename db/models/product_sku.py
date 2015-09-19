from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
     
class ProductSku(models.Model):
    product_item = models.ForeignKey("ProductItem", verbose_name=_("Product Item"), related_name='product_skus', blank=True, null=True)
    sku = models.CharField(_("Sku"), max_length=50, blank=True)
    item_number = models.CharField(_("Item Number"), max_length=50, blank=True)
    style = models.CharField(_("Style"), max_length=50, blank=True)
    description = models.CharField(_("Description"), max_length=50, blank=True)
    size = models.CharField(_("Size"), max_length=50, blank=True)
    upc = models.CharField(_("UPC"), max_length=50, blank=True)
    cost = models.DecimalField(_("Cost"), max_digits=7, decimal_places=2, default=0, blank=False)
    wholesale = models.DecimalField(_("Wholesale"), max_digits=7, decimal_places=2, default=0, blank=False)
    msrp = models.DecimalField(_("MSRP"), max_digits=7, decimal_places=2, default=0, blank=False)
    inventory = models.IntegerField(_('Inventory'), null=False, blank=False, default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s %s" % (self.sku, self.style, self.description)
        
    def convert_to_dict(self):
        return {
            "id": self.pk,
            "productItemId": self.product_item.pk,
            "sku": self.sku,
            "itemNumber": self.item_number,
            "style": self.style,
            "description": self.description,
            "size": self.size,
            "upc": self.upc,
            "cost": self.cost,
            "wholesale": self.wholesale,
            "msrp": self.msrp,
            "inventory": self.inventory,
            "active": self.active,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "Product Sku"
        verbose_name_plural = "Product Skus"
        ordering = ["sku"]