from django.db import models

class Category(models.Model):
    label = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.label
