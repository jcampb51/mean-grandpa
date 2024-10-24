from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from grandpaapi.models import ExerciseCategory

class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = ['id', 'category_id', 'exercise_id']  # Assuming your ExerciseCategory model has these fields

class ExerciseCategories(ViewSet):
    """
    A simple ViewSet for listing or retrieving exercise categories.
    """

    def list(self, request):
        """List all exercise categories"""
        categories = ExerciseCategory.objects.all()
        serializer = ExerciseCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve a single exercise category"""
        try:
            category = ExerciseCategory.objects.get(pk=pk)
            serializer = ExerciseCategorySerializer(category)
            return Response(serializer.data)
        except ExerciseCategory.DoesNotExist:
            return Response({"error": "Exercise Category not found"}, status=status.HTTP_404_NOT_FOUND)