from django.db import models


class MediaPlayerSlide(models.Model):
    SLIDE_TYPE = (
        ("IMAGE", "Image"),
        ("YOUTUBE", "YouTube Video"),
        ("VIMEO", "Vimeo Video"),
    )
    
    media_player = models.ForeignKey("MediaPlayer", verbose_name="Media Player", related_name='media_player_slides', null=True)
    media_file = models.ForeignKey("MediaFile", verbose_name="Media File", related_name='media_player_slides', null=True)
    slide_type = models.CharField(default="IMAGE", choices=SLIDE_TYPE, max_length=30)
    title = models.CharField("Title", max_length=100, null=True)
    video_code = models.CharField("Video Code", max_length=50, null=True)
    sort_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
        
    class Meta:
        app_label = "db"
        verbose_name = "Media Player Slide"
        verbose_name_plural = "Media Player Slides"
        ordering = ["title"]