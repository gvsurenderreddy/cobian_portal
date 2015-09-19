from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone
from django.db import models
     
class Message(models.Model):
    MESSAGE_TYPE = (
        ("EVERYONE", "Everyone"),
        ("DEALER", "Dealer"),
        ("REP", "Rep"),
    )
    
    message_type = models.CharField(_("Message for"), default="EVERYONE", choices=MESSAGE_TYPE, max_length=20)
    message_date = models.DateTimeField(_("Message date"), blank=True, null=True, default=timezone.now())
    title = models.CharField(_("Title"), blank=True, null=True, max_length=30)
    message = models.TextField(_("Message"), blank=True, null=True)
    enabled = models.BooleanField(default=False)
 
    def __str__(self):
        return "%s - %s (%s): %s" % (self.pk, self.title, self.message_date, self.enabled)
        
    class Meta:
        app_label = "db"
        verbose_name = "Message"
        verbose_name_plural = "Messages"