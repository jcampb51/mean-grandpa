from django.db import models
from .exercise import Exercise
from .workout import Workout
from django.contrib.auth.models import User

class Log(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    weight = models.IntegerField()
    reps = models.IntegerField()
    sets = models.IntegerField()
    interval = models.IntegerField()

    def __str__(self):
        return f"Log for {self.exercise.name}"
