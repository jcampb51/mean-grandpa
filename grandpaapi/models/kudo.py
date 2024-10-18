from django.db import models

class Kudo(models.Model):
    label = models.CharField(max_length=50)
    img = models.URLField()

    def __str__(self):
        return self.label
