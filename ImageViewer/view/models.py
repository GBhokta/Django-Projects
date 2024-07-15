from django.db import models
from django.utils.translation import gettext_lazy as _

class Image(models.Model):
    photo = models.ImageField(_("photo"), upload_to="my_image", height_field=None, width_field=None, max_length=None)
    date = models.DateTimeField(_("date"), auto_now_add=True)

    def __str__(self):
        return f"Image taken on {self.date}"
