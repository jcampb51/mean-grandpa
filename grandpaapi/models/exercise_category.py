from django.db import models
from .exercise import Exercise
from .category import Category

class ExerciseCategory(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exercise.name} in {self.category.label}"
