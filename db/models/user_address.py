from django.db import models


class UserAddress(models.Model):
    ADDRESS_TYPE = (
        ("BILLTO", "Bill To"),
        ("SHIPTO", "Ship To"),
    )
    
    user_profile = models.ForeignKey("UserProfile", related_name='addresses', blank=True, null=True)
    address_type = models.CharField(default="BILLTO", choices=ADDRESS_TYPE, max_length=20)
    name = models.CharField("Name", max_length=200, blank=True, null=True)
    address_id = models.CharField("Address ID", max_length=200, blank=True, null=True)
    address1 = models.CharField("Address",max_length=50, blank=True, null=True)
    address2 = models.CharField("Address", max_length=50, blank=True, null=True)
    city = models.CharField("City", max_length=50, blank=True, null=True)
    state = models.CharField("State", max_length=30, blank=True, null=True)
    postal_code = models.CharField("Postal Code", blank=True, null=True, max_length=9)
    country = models.CharField("Country", blank=True, null=True, max_length=30)
    
    def __str__(self):
        return "{} {}".format(self.address_type, self.address1)
            
    def convert_to_dict(self):
        return {
            "id": self.pk,
            "userProfileId": self.user_profile.pk,
            "addressType": self.address_type,
            "name": self.name,
            "addressId": self.address_id,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "state": self.state,
            "postalCode": self.postal_code,
            "country": self.country,
        }
        
    class Meta:
        app_label = "db"
        verbose_name = "User Address"
        verbose_name_plural = "User Addresses"
