from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
     
class DataOption(models.Model):
    OPTION_TYPE = (
        ("PRE-BOOK", "Pre-Book Options"),
    )
    
    option_type = models.CharField(default="PRE-BOOK", choices=OPTION_TYPE, max_length=20)
    description = models.CharField(_("Description"), max_length=50, blank=True, null=True, default="")
    value = models.CharField(_("Value"), max_length=100, blank=True)
    sort_order = models.IntegerField(_('Sort Order'), null=False, blank=False, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s: %s - %s" % (self.option_type, self.description, self.value)
        
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