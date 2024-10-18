from django.db import models
from .workout import Workout
from .category import Category

class WorkoutCategory(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Workout {self.workout.id} in {self.category.label}"
