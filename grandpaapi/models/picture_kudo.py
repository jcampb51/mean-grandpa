from django.db import models
from .picture import Picture
from .kudo import Kudo
from django.contrib.auth.models import User

class PictureKudo(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    kudo = models.ForeignKey(Kudo, on_delete=models.CASCADE)
    giver = models.ForeignKey(User, related_name='giver', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)

    def __str__(self):
        return f"Kudo on {self.picture.img_source} by {self.giver.username}"
