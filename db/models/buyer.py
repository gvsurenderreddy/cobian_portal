from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
     
class Buyer(models.Model):
    BUYER_TYPE = (
        ("KIDS", "Kids"),
        ("MENS", "Mens"),
        ("WOMENS", "Womens"),
    )
    
    user_profile = models.ForeignKey("UserProfile", related_name='buyers', blank=True, null=True)
    buyer_type = models.CharField(default="KIDS", choices=BUYER_TYPE, max_length=20)
    name = models.CharField(_("Name"), max_length=100, blank=True)
    phone = models.CharField(_("Phone Number"), blank=True, null=True, max_length=30)
    email = models.CharField(_("Email"), blank=True, null=True, max_length=100)
    not_available = models.BooleanField(_("Not Available"), default=False)
    
    def __str__(self):
        return "%s - %s %s" % (self.pk, self.name, self.buyer_type)
        
    class Meta:
        app_label = "db"
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"
        ordering = ["name"]