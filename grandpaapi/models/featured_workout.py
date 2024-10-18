from django.db import models
from .workout import Workout

class FeaturedWorkout(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=20)
    split = models.BooleanField(default=False)
    current = models.BooleanField(default=False)

    def __str__(self):
        return f"Featured workout: {self.weekday}"
