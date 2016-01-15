import time

from django.db import models


class WarrantyHistory(models.Model):
    warranty = models.ForeignKey("Warranty", verbose_name="Warranty", related_name='warranty_history')
    user_profile = models.ForeignKey("UserProfile", verbose_name="User Profile", related_name='warranty_history')
    action = models.CharField("Action", max_length=255)
    action_date = models.DateTimeField("Action Date", auto_now_add=True)

    def __str__(self):
        return "{} - {}: {}".format(self.warranty.claim_number, self.action, self.action_date)

    def convert_to_dict(self):
        return {
            "id": self.pk,
            "userId": self.user_profile.user.pk,
            "userProfileId": self.user_profile.pk,
            "user": "{} {}".format(self.user_profile.user.first_name, self.user_profile.user.last_name),
            "warrantyId": self.warranty.pk,
            "action": self.action,
            "actionDate": time.mktime(self.action_date.timetuple())
        }

    class Meta:
        app_label = "db"
        verbose_name = "Warranty History"
        verbose_name_plural = "Warranty History"
        ordering = ["action_date"]
