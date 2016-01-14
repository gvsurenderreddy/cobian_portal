from django.db import models
from datetime import datetime


class Message(models.Model):
    MESSAGE_TYPE = (
        ("EVERYONE", "Everyone"),
        ("DEALER", "Dealer"),
        ("REP", "Rep"),
    )
    
    message_type = models.CharField("Message for", default="EVERYONE", choices=MESSAGE_TYPE, max_length=20)
    message_date = models.DateTimeField("Message date", blank=True, null=True, default=datetime.now())
    title = models.CharField("Title", null=True, max_length=30)
    message = models.TextField("Message", null=True)
    enabled = models.BooleanField(default=False)
 
    def __str__(self):
        return "{} - {} ({}): {}".format(self.pk, self.title, self.message_date, self.enabled)
        
    class Meta:
        app_label = "db"
        verbose_name = "Message"
        verbose_name_plural = "Messages"
