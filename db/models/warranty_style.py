from django.db import models


class WarrantyStyle(models.Model):
    style = models.CharField("Style", max_length=50, blank=True, null=True)

    def __str__(self):
        return self.style

    def convert_to_dict(self):
        return {
            "id": self.pk,
            "style": self.style,
        }

    class Meta:
        app_label = "db"
        verbose_name = "Warranty Style"
        verbose_name_plural = "Warranty Styles"
        ordering = ["style"]