from django.db import models
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer
from tagging.fields import TagField


class MediaFile(models.Model):
    FILE_TYPE = (
            ("AD", "Ad"),
            ("MEDIA_PLAYER", "Media Player"),
            ("PRODUCT", "Product"),
    )
    
    title = models.CharField("Title", max_length=100, null=True)
    file_type = models.CharField(default="AD", choices=FILE_TYPE, max_length=20)
    file_path = models.FileField(upload_to="media_file/%Y/%m/%d")
    file_name = models.CharField("File Name", max_length=50, null=True)
    file_extension = models.CharField("File Extension", max_length=10, null=True)
    description = models.CharField("Description", max_length=255, null=True)
    uploaded = models.DateField(auto_now=False, auto_now_add=True)
    tags = TagField()

    def __str__(self):
        return self.title

    def save(self):
        file_path = self.file_path.url
        file_extension = "???"
        file_name = file_path
        
        # parse file name
        position = file_path.rfind("/")
        if position > -1:
            file_name = file_path[position+1:]
        self.file_name = file_name
        
        # parse file extension
        position = file_path.rfind(".")
        if position > -1:
            file_extension = file_path[position+1:].upper()
        self.file_extension = file_extension
        
        super(MediaFile, self).save()

    def thumbnail(self):
        return_value = '<img src="{}{}" alt=""/>'.format(settings.STATIC_URL, "images/unknown-icon.png")
        if self.file_path:
            if self.file_extension == "JPG" or self.file_extension == "JPEG" \
                    or self.file_extension == "PNG" or self.file_extension == "GIF":
                thumbnailer = get_thumbnailer(self.file_path)
                thumbnail = thumbnailer.get_thumbnail({'size': (120, 90), 'crop': True})
                return_value = '<img src="{}{}" alt=""/>'.format(settings.MEDIA_URL, thumbnail)
            elif self.file_extension == "PDF":
                return_value = '<img src="{}{}" alt=""/>'.format(settings.STATIC_URL, "images/PDF-icon.png")
            elif self.file_extension == "TXT":
                return_value = '<img src="{}{}" alt=""/>'.format(settings.STATIC_URL, "images/TXT-icon.png")
            elif self.file_extension == "DOC" or self.file_extension == "DOCX":
                return_value = '<img src="{}{}" alt=""/>'.format(settings.STATIC_URL, "images/DOC-icon.png")
            elif self.file_extension == "ZIP":
                return_value = '<img src="{}{}" alt=""/>'.format(settings.STATIC_URL, "images/ZIP-icon.png")
            else:
                return '<img src="{}{}" alt=""/>'.format(settings.STATIC_URL, "images/unknown-icon.png")

        return return_value
    thumbnail.short_file_extension = "Thumbnail"
    thumbnail.allow_tags = True

    class Meta:
        app_label = "db"
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"
        ordering = ["title"]
