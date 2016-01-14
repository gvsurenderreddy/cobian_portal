import time

from django.db import models


class Warranty(models.Model):
    STATUS = (
        ("NEW", "New Claim"),
        ("PREAUTHORIZED", "Pre-Authorized"),
        ("RECEIVED", "Received"),
        ("AUTHORIZED", "Authorized"),
        ("NOTAUTHORIZED", "Not Authorized"),
        ("CLOSED", "Closed"),
    )

    claim_number = models.CharField("Claim Number", max_length=50, blank=True, null=True)
    status = models.CharField(default="NEW", choices=STATUS, max_length=20)
    status_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField("Name", max_length=100, blank=True, null=True)
    email = models.CharField("Email", max_length=100, blank=True, null=True)
    phone = models.CharField("Phone", max_length=50, blank=True, null=True)
    address = models.CharField("Address", max_length=100, blank=True, null=True)
    style = models.CharField("Style", max_length=50, blank=True, null=True)
    color = models.CharField("Color", max_length=50, blank=True, null=True)
    damage = models.CharField("Damage", max_length=100, blank=True, null=True)
    image_override = models.BooleanField("Image Override", default=False)
    email_sent = models.BooleanField("Email Sent", default=False)
    notes = models.TextField("Notes", blank=True, null=True)

    def __str__(self):
        return "{} - {}: {}".format(self.claim_number, self.status, self.status_date)

    def convert_to_dict(self):
        status_description = "Unknown"
        for value, description in self.STATUS:
            if value == self.status:
                status_description = description

        return {
            "id": self.pk,
            "claimNumber": self.claim_number,
            "status": self.status,
            "statusDescription": status_description,
            "statusDate": time.mktime(self.status_date.timetuple()),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "style": self.style,
            "color": self.color,
            "damage": self.damage,
            "imageOverride": self.image_override,
            "emailSent": self.email_sent,
            "notes": self.notes,
        }

    class Meta:
        app_label = "db"
        verbose_name = "Warranty"
        verbose_name_plural = "Warranties"
        ordering = ["status_date"]
