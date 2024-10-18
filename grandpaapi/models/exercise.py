from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    video_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
