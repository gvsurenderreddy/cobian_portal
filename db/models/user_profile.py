from django.db import models
from django.contrib.auth.models import User


def get_terms_upload_to(instance, filename):
    return "terms/{}/{}".format(instance.pk, filename)


class UserProfile(models.Model):
    USER_TYPE = (
        ("ADMIN", "Administrator"),
        ("CUSTOMER_SERVICE", "Customer Service"),
        ("DEALER", "Dealer"),
        ("REP", "Rep"),
    )
    
    user = models.OneToOneField(User)
    user_type = models.CharField(default="DEALER", choices=USER_TYPE, max_length=20)
    account_id = models.CharField("Account Id",max_length=50, blank=True, null=True)
    account_rep = models.ForeignKey('self', related_name="rep", blank=True, null=True)
    company = models.CharField("Company", max_length=100, blank=True, null=True)
    phone = models.CharField("Phone Number", blank=True, null=True, max_length=30)
    terms = models.CharField("Terms",max_length=50, blank=True, null=True)
    shipping_method = models.CharField("Shipping Method",max_length=50, blank=True, null=True)
    discount = models.DecimalField("Discount", max_digits=4, decimal_places=2, default=0, null=False)
    notes = models.TextField(default="", blank=True, null=True)
    create_date = models.DateField(auto_now=False, auto_now_add=True)
    locked = models.BooleanField(default=False)
    terms_accepted = models.BooleanField("Terms Accepted", default=False)
    terms_uploaded = models.BooleanField("Terms Uploaded", default=False)
    terms_file_path = models.FileField(upload_to=get_terms_upload_to, blank=True, null=True)
    eula_accepted = models.BooleanField("EULA Accepted", default=False)
    warranty_receiver = models.BooleanField("Warranty Receiver Role", default=False)
    warranty_authorizer = models.BooleanField("Warranty Authorizer Role", default=False)
    
    def convert_to_dict(self):
        account_rep_id = 0
        if self.account_rep:
            account_rep_id = self.account_rep.pk
            
        return {
            "id": self.pk,
            "userId": self.user.pk,
            "userType": self.user_type,
            "userName": self.user.username,
            "firstName": self.user.first_name,
            "lastName": self.user.last_name,
            "email": self.user.email,
            "accountRepId": account_rep_id,
            "accountId": self.account_id,
            "name": self.company,
            "phone": self.phone,
            "terms": self.terms,
            "shipping_method": self.shipping_method,
            "discount": self.discount,
            "notes": self.notes,
            "warrantyReceiver": self.warranty_receiver,
            "warrantyAuthorizer": self.warranty_authorizer,
        }
        
    def __str__(self):
        return "{} - {}".format(self.pk, self.company)
            
    class Meta:
        app_label = "db"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        
    def user_name(self):
        return "{} - {} {}".format(self.account_id, self.user.first_name, self.user.last_name)