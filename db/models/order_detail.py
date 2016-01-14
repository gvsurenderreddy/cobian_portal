from django.db import models


class OrderDetail(models.Model):
    order = models.ForeignKey("Order", verbose_name="Order", related_name='order_details', blank=True, null=True)
    quantity = models.IntegerField("Quantity", default=1, blank=True, null=True)
    sku = models.CharField("Sku", max_length=50, blank=True, null=True)
    item_number = models.CharField("Item Number", max_length=50, blank=True, null=True)
    style = models.CharField("Style", max_length=50, blank=True, null=True)
    description = models.CharField("Description", max_length=50, blank=True, null=True)
    size = models.CharField("Size", max_length=50, blank=True, null=True)
    upc = models.CharField("UPC", max_length=50, blank=True, null=True)
    cost = models.DecimalField("Cost", max_digits=7, decimal_places=2, default=0, null=False)
    price = models.DecimalField("Price", max_digits=7, decimal_places=2, default=0, null=False)

    def __str__(self):
        return "{} - {} {}".format(self.sku, self.style, self.description)
    
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