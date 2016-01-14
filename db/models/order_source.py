from django.db import models


class OrderSource(models.Model):
    description = models.CharField("Description", max_length=50, blank=True, null=True, default="",
                                   help_text="Description displayed on order screen")
    value = models.CharField("Value", max_length=100, blank=True, null=True, help_text="Value attached to order")
    sort_order = models.IntegerField("Sort Order", null=False, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.description, self.value)
        
    def convert_to_dict(self):
        return {
            "id": self.pk,
            "description": self.description,
            "value": self.value,
            "sortOrder": self.sort_order,
            "active": self.active,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "Order Source"
        verbose_name_plural = "Order Sources"
        ordering = ["sort_order"]