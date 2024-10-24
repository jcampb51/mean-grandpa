from django.db import models
from .post import Post
from django.contrib.auth.models import User

class Picture(models.Model):
    user = models.ForeignKey(User, related_name="pictures", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="pictures", on_delete=models.CASCADE)
    img_source = models.CharField(max_length=255)
    upload_date = models.DateTimeField()

    def __str__(self):
        return f"Picture for post {self.post.title}"
