from django.db import models


class ProductSku(models.Model):
    product_item = models.ForeignKey("ProductItem", verbose_name="Product Item", related_name='product_skus', blank=True, null=True)
    sku = models.CharField("Sku", max_length=50, blank=True, null=True)
    item_number = models.CharField("Item Number", max_length=50, blank=True, null=True)
    style = models.CharField("Style", max_length=50, blank=True, null=True)
    description = models.CharField("Description", max_length=50, blank=True, null=True)
    size = models.CharField("Size", max_length=50, blank=True, null=True)
    upc = models.CharField("UPC", max_length=50, blank=True, null=True)
    cost = models.DecimalField("Cost", max_digits=7, decimal_places=2, default=0, null=False)
    wholesale = models.DecimalField("Wholesale", max_digits=7, decimal_places=2, default=0, null=False)
    msrp = models.DecimalField("MSRP", max_digits=7, decimal_places=2, default=0, null=False)
    inventory = models.IntegerField("Inventory", null=False, default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} {}".format(self.sku, self.style, self.description)
        
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
