from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_link = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title
