from django.db import models
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer


def get_file_path_upload_to(instance, filename):
    return 'warranty_images/{}/{}'.format(instance.warranty.pk, filename)


class WarrantyImage(models.Model):
    TYPE = (
        ("PROOF", "Proof of Purchase"),
        ("IMAGE", "Product Image"),
    )

    warranty = models.ForeignKey("Warranty", related_name='images', blank=True, null=True)
    type = models.CharField(default="PROOF", choices=TYPE, max_length=20)
    title = models.CharField("Title", max_length=100, blank=True, null=True)
    file_path = models.FileField(upload_to=get_file_path_upload_to)
    file_name = models.CharField("File Name", max_length=50, blank=True, null=True)
    file_extension = models.CharField("File Extension", max_length=10, blank=True, null=True)
    description = models.CharField("Description", max_length=255, blank=True, null=True)
    uploaded = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.warranty.pk, self.description)

    def convert_to_dict(self):
        type_description = "Unknown"
        for value, description in self.TYPE:
            if value == self.type:
                type_description = description

        return {
            "id": self.pk,
            "warrantyId": self.warranty.pk,
            "type": self.type,
            "typeDescription": type_description,
            "title": self.title,
            "filePath": self.file_path.url,
            "fileName": self.file_name,
            "fileExtension": self.file_extension,
            "description": self.description,
            "uploadDate": self.uploaded.strftime('%m/%d/%Y'),
        }

    def save(self):
        file_path = self.file_path.url
        file_extension = "???"
        file_name = file_path

        # parse file name
        position = file_path.rfind("/")
        if position > -1:
            file_name = file_path[position+1:]
        self.title = file_name
        self.file_name = file_name

        # parse file extension
        position = file_path.rfind(".")
        if position > -1:
            file_extension = file_path[position+1:].upper()
        self.file_extension = file_extension

        super(WarrantyImage, self).save()

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

    class Meta:
        app_label = "db"
        verbose_name = "Warranty Image"
        verbose_name_plural = "Warranty Images"
        ordering = ["title"]