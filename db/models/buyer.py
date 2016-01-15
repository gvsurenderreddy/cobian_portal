from django.db import models


class Buyer(models.Model):
    BUYER_TYPE = (
        ("KIDS", "Kids"),
        ("MENS", "Mens"),
        ("WOMENS", "Womens"),
    )
    
    user_profile = models.ForeignKey("UserProfile", related_name='buyers', null=False)
    buyer_type = models.CharField(default="KIDS", choices=BUYER_TYPE, max_length=20)
    name = models.CharField("Name", max_length=100, null=True)
    phone = models.CharField("Phone Number", null=True, max_length=30)
    email = models.CharField("Email", null=True, max_length=100)
    not_available = models.BooleanField("Not Available", default=False)
    
    def __str__(self):
        return "{} - {} {}".format(self.pk, self.name, self.buyer_type)
        
    class Meta:
        app_label = "db"
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"
        ordering = ["name"]