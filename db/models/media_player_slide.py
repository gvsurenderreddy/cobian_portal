from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
     
class MediaPlayerSlide(models.Model):
    SLIDE_TYPE = (
        ("IMAGE", "Image"),
        ("YOUTUBE", "YouTube Video"),
        ("VIMEO", "Vimeo Video"),
    )
    
    media_player = models.ForeignKey("MediaPlayer", verbose_name=_("Media Player"), related_name='media_player_slides', blank=True, null=True)
    media_file = models.ForeignKey("MediaFile", verbose_name=_("Media File"), related_name='media_player_slides', blank=True, null=True)
    slide_type = models.CharField(default="IMAGE", choices=SLIDE_TYPE, max_length=30)
    title = models.CharField(_("Title"), max_length=100, blank=True)
    video_code = models.CharField(_("Video Code"), max_length=50, blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
        
    class Meta:
        app_label = "db"
        verbose_name = "Media Player Slide"
        verbose_name_plural = "Media Player Slides"
        ordering = ["title"]