# workouts.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status
from django.http import HttpResponseForbidden
from django.db import transaction
from django.utils import timezone
from grandpaapi.models import Workout, WorkoutExercise, WorkoutCategory, Exercise, Category, Log


# Serializers
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'video_link']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label', 'description']

class LogSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = Log
        fields = ['id', 'weight', 'reps', 'sets', 'interval', 'exercise']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = [
            'id', 'date_created', 'target_date', 'completed', 'featured',
            'exercises', 'categories', 'logs'
        ]

    def get_exercises(self, obj):
        exercises = Exercise.objects.filter(workoutexercise__workout=obj)
        return ExerciseSerializer(exercises, many=True).data

    def get_categories(self, obj):
        categories = Category.objects.filter(workoutcategory__workout=obj)
        return CategorySerializer(categories, many=True).data

    def get_logs(self, obj):
        logs = Log.objects.filter(workout=obj)  # Retrieve logs specifically tied to this workout
        return LogSerializer(logs, many=True).data
    
class WorkoutCreateSerializer(serializers.ModelSerializer):
    exercises = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    category = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'date_created', 'target_date', 'completed', 'featured', 'exercises', 'category']


# ViewSet
class Workouts(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # List workouts for current user or all if staff
        if request.user.is_staff:
            workouts = Workout.objects.all()
        else:
            workouts = Workout.objects.filter(user=request.user)

        serializer = WorkoutSerializer(workouts, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            workout = Workout.objects.get(pk=pk)
            if workout.user != request.user and not request.user.is_staff:
                return HttpResponseForbidden("You can only view your own workouts.")

            serializer = WorkoutSerializer(workout, context={'request': request})
            return Response(serializer.data)
        except Workout.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get_next_scheduled_workout(self, request):
        # Get the next scheduled workout for the user where 'completed' is False and order by 'target_date'
        try:
            workout = Workout.objects.filter(user=request.user, completed=False, target_date__gte=timezone.now())\
                                     .order_by('target_date').first()
            if not workout:
                return Response({"message": "No upcoming workouts scheduled."}, status=status.HTTP_404_NOT_FOUND)

            serializer = WorkoutSerializer(workout, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_workout_logs(self, request, pk=None):
        # Get logs for the specific workout
        try:
            workout = Workout.objects.get(pk=pk, user=request.user)
            logs = Log.objects.filter(workout=workout)
            serializer = LogSerializer(logs, many=True, context={'request': request})
            return Response(serializer.data)
        except Workout.DoesNotExist:
            return Response({"error": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic  # Ensure atomicity, so either all or nothing is committed
    def create(self, request):
        # Parse data
        target_date = request.data.get('target_date')
        category_id = request.data.get('category')
        exercise_ids = request.data.get('exercises')

        # Ensure category and exercises exist
        try:
            category = Category.objects.get(pk=category_id)
            exercises = Exercise.objects.filter(id__in=exercise_ids)
            if len(exercises) != len(exercise_ids):
                return Response({"error": "One or more exercises do not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Category does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Create workout
        workout = Workout.objects.create(
            user=request.user,
            target_date=target_date,
            completed=False,  # Initially not completed
            featured=False    # Set to False unless otherwise specified
        )

        # Create workout category
        WorkoutCategory.objects.create(workout=workout, category=category)

        # Create workout exercises and empty logs
        for exercise in exercises:
            workout_exercise = WorkoutExercise.objects.create(workout=workout, exercise=exercise)
            Log.objects.create(user=request.user, exercise=exercise, workout=workout, weight=0, reps=0, sets=0, interval=0)

        # Serialize the newly created workout
        serializer = WorkoutSerializer(workout, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic  # Ensure atomicity, so either all or nothing is committed
    def update(self, request, pk=None):
        try:
            workout = Workout.objects.get(pk=pk)
            
            # Ensure the user is the owner or staff
            if workout.user != request.user and not request.user.is_staff:
                return HttpResponseForbidden("You can only update your own workouts.")
            
            # Parse data
            target_date = request.data.get('target_date')
            category_id = request.data.get('category')
            exercise_ids = request.data.get('exercises')

            # Ensure category and exercises exist
            try:
                category = Category.objects.get(pk=category_id)
                exercises = Exercise.objects.filter(id__in=exercise_ids)
                if len(exercises) != len(exercise_ids):
                    return Response({"error": "One or more exercises do not exist."}, status=status.HTTP_400_BAD_REQUEST)
            except Category.DoesNotExist:
                return Response({"error": "Category does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Update workout fields
            workout.target_date = target_date
            workout.save()

            # Update workout category
            WorkoutCategory.objects.filter(workout=workout).delete()  # Remove existing category
            WorkoutCategory.objects.create(workout=workout, category=category)  # Add new category

            # Update workout exercises and logs
            existing_exercise_ids = WorkoutExercise.objects.filter(workout=workout).values_list('exercise_id', flat=True)

            # Remove old workout exercises and logs not in the new list
            WorkoutExercise.objects.filter(workout=workout).exclude(exercise_id__in=exercise_ids).delete()
            
            # Remove logs for exercises no longer part of the workout
            Log.objects.filter(workout=workout).exclude(exercise_id__in=exercise_ids).delete()

            # Add new workout exercises and logs if they don't already exist
            for exercise in exercises:
                if exercise.id not in existing_exercise_ids:
                    # Create WorkoutExercise entry
                    WorkoutExercise.objects.create(workout=workout, exercise=exercise)
                    # Create an empty Log entry for the new exercise
                    Log.objects.create(user=request.user, exercise=exercise, workout=workout, weight=0, reps=0, sets=0, interval=0)

            # Serialize the updated workout
            serializer = WorkoutSerializer(workout, context={'request': request})
            return Response(serializer.data)
    
        except Workout.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk=None):
        try:
            workout = Workout.objects.get(pk=pk)
            if workout.user != request.user and not request.user.is_staff:
                return HttpResponseForbidden("You can only delete your own workouts.")

            # Delete related join table entries
            WorkoutExercise.objects.filter(workout=workout).delete()
            WorkoutCategory.objects.filter(workout=workout).delete()
            Log.objects.filter(workout=workout).delete()  # Also delete logs tied to the workout
            workout.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Workout.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
