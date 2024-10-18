from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_access = models.BooleanField(default=False)
    post_access = models.BooleanField(default=False)
    profile_access = models.BooleanField(default=False)
    kudos_access = models.BooleanField(default=False)
    admin_lock = models.BooleanField(default=False)
    is_minor = models.BooleanField(default=False)
    dob = models.DateField()
    picture = models.URLField(blank=True, null=True)
    paid_client = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"
