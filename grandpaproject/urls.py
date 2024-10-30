from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from grandpaapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", Users, "user")
router.register(r"exercises", Exercises, "exercise")
router.register(r"logs", Logs, "log")
router.register(r"categories", Categories, "category")
router.register(r"exercise-categories", ExerciseCategories, "exercise-category")
router.register(r'featured_workouts', FeaturedWorkouts, "featured_workout")

workout_list = Workouts.as_view({
    'get': 'list',
    'post': 'create'
})

workout_detail = Workouts.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# Add a separate path for the copy_workout action
workout_copy = Workouts.as_view({
    'post': 'copy_workout'
})

urlpatterns = [
    path('', include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    
    # Workout routes
    path('workouts/next', Workouts.as_view({'get': 'get_next_scheduled_workout'}), name='next_scheduled_workout'),
    path('workouts/<int:pk>/logs', Workouts.as_view({'get': 'get_workout_logs'}), name='workout_logs'),
    path('workouts/', workout_list, name='workout-list'),
    path('workouts/<int:pk>/', workout_detail, name='workout-detail'),
    
    # Copy workout route
    path('workouts/<int:pk>/copy_workout', workout_copy, name='copy-workout')
]
