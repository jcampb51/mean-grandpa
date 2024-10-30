# views/featured_workouts.py

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from grandpaapi.models import FeaturedWorkout
from grandpaapi.views import WorkoutSerializer
from django.http import HttpResponseForbidden

# Serializer for FeaturedWorkout
class FeaturedWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedWorkout
        fields = ['id', 'workout', 'weekday', 'split', 'current']

# ViewSet for managing featured workouts
class FeaturedWorkouts(ViewSet):
    
    def create(self, request):
        """Handles creation of a new featured workout"""
        if not request.user.is_staff:
            return HttpResponseForbidden("Only staff can feature workouts.")
        
        serializer = FeaturedWorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """Handles updating an existing featured workout"""
        try:
            featured_workout = FeaturedWorkout.objects.get(pk=pk)
            if not request.user.is_staff:
                return HttpResponseForbidden("Only staff can modify featured workouts.")

            serializer = FeaturedWorkoutSerializer(featured_workout, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FeaturedWorkout.DoesNotExist:
            return Response({"error": "Featured workout not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handles listing featured workouts with filter options for split and current status"""
        split = request.query_params.get('split') == 'true'
        current = request.query_params.get('current') == 'true'
        
        featured_workouts = FeaturedWorkout.objects.filter(split=split, current=current)
        serialized_workouts = WorkoutSerializer([fw.workout for fw in featured_workouts], many=True)
        
        return Response(serialized_workouts.data)
