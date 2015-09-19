from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
     
class ProductStyle(models.Model):
    style_sku = models.CharField(_("Style Sku"), max_length=50, blank=True)
    style = models.CharField(_("Style"), max_length=50, blank=True)

    def __str__(self):
        return "%s - %s" % (self.style_sku, self.style)
        
    def convert_to_dict(self):
        return {
            "id": self.pk,
            "styleSku": self.style_sku,
            "style": self.style,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "Product Style"
        verbose_name_plural = "Product Styles"
        ordering = ["style_sku"]