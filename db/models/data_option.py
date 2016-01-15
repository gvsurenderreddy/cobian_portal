from django.db import models


class DataOption(models.Model):
    OPTION_TYPE = (
        ("PRE-BOOK", "Pre-Book Options"),
        ("WARRANTY_DAMAGE", "Warranty Damage"),
    )
    
    option_type = models.CharField(default="PRE-BOOK", choices=OPTION_TYPE, max_length=20)
    description = models.CharField("Description", max_length=50, null=True, default="")
    value = models.CharField("Value", max_length=100, null=True)
    sort_order = models.IntegerField("Sort Order", null=False, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}: {} - {}".format(self.option_type, self.description, self.value)
        
    def convert_to_dict(self):
        return {
            "id": self.pk,
            "optionType": self.option_type,
            "description": self.description,
            "value": self.value,
            "sortOrder": self.sort_order,
            "active": self.active,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "Data Option"
        verbose_name_plural = "Data Options"
        ordering = ["option_type"]