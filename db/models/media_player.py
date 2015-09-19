from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
     
class MediaPlayer(models.Model):
    AUDIENCE = (
        ("EVERYONE", "Everyone"),
        ("DEALER", "Dealer"),
        ("REP", "Rep"),
    )
    
    audience = models.CharField(default="ALL", choices=AUDIENCE, max_length=30)
    title = models.CharField(_("Title"), max_length=100, blank=True)
    enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
        
    class Meta:
        app_label = "db"
        verbose_name = "Media Player"
        verbose_name_plural = "Media Players"
        ordering = ["title"]