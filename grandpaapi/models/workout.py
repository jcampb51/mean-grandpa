from django.db import models
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField()
    completed = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Workout on {self.target_date}"