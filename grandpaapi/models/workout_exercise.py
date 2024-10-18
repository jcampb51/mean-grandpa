from django.db import models
from .workout import Workout
from .exercise import Exercise

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"Exercise {self.exercise.name} in workout {self.workout.id}"
