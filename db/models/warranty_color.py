from django.db import models


class WarrantyColor(models.Model):
    color = models.CharField("Color", max_length=50, blank=True, null=True)

    def __str__(self):
        return self.color

    def convert_to_dict(self):
        return {
            "id": self.pk,
            "color": self.color,
        }

    class Meta:
        app_label = "db"
        verbose_name = "Warranty Color"
        verbose_name_plural = "Warranty Colors"
        ordering = ["color"]