from django.db import models
from .post import Post
from django.contrib.auth.models import User

class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    img_source = models.URLField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture for post {self.post.title}"
