# exercises.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status
from django.http import HttpResponseForbidden
from grandpaapi.models import Exercise, ExerciseCategory, Category, Log

# Serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label', 'description']

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'weight', 'reps', 'sets', 'interval']

class ExerciseSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'video_link', 'categories', 'logs']

    def get_categories(self, obj):
        categories = Category.objects.filter(exercisecategory__exercise=obj)
        return CategorySerializer(categories, many=True).data

    def get_logs(self, obj):
        user = self.context['request'].user
        logs = Log.objects.filter(exercise=obj, user=user)
        return LogSerializer(logs, many=True).data

# ViewSet
class Exercises(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            exercise = Exercise.objects.get(pk=pk)
            serializer = ExerciseSerializer(exercise, context={'request': request})
            return Response(serializer.data)
        except Exercise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        if not request.user.is_staff:
            return HttpResponseForbidden("Only staff can create exercises.")

        serializer = ExerciseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            exercise = serializer.save()
            # Handle categories association if needed
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if not request.user.is_staff:
            return HttpResponseForbidden("Only staff can update exercises.")

        try:
            exercise = Exercise.objects.get(pk=pk)
            serializer = ExerciseSerializer(exercise, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                # Handle categories association if needed
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exercise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        if not request.user.is_staff:
            return HttpResponseForbidden("Only staff can delete exercises.")

        try:
            exercise = Exercise.objects.get(pk=pk)
            exercise.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exercise.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
