from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
from datetime import datetime
     
class ProductItem(models.Model):
    product_style = models.ForeignKey("ProductStyle", verbose_name=_("Product Style"), related_name='product_items', blank=True, null=True)
    item_number = models.CharField(_("Item Number"), max_length=50, blank=True)
    description = models.CharField(_("Description"), max_length=50, blank=True)
    image_path = models.ImageField(upload_to="product_images", blank=True, null=True)
    available = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.item_number, self.description)
        
    def convert_to_dict(self):
        image_path = None
        if self.image_path:
            image_path = self.image_path.url
            
        available_date = datetime.now().strftime('%m/%d/%Y')
        if self.available:
            available_date = self.available.strftime('%m/%d/%Y')
        return {
            "id": self.pk,
            "productStyleId": self.product_style.pk,
            "itemNumber": self.item_number,
            "description": self.description,
            "imagePath": image_path,
            "available": available_date,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "Product Item"
        verbose_name_plural = "Product Items"
        ordering = ["item_number"]