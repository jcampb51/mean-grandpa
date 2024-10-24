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
router.register(r"exercise-categories", ExerciseCategories, "exercise-category")  # Registering the new viewset


urlpatterns = [
    path('', include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    

    # Workout routes (supporting GET, POST, PUT, DELETE)
    path('workouts/next', Workouts.as_view({'get': 'get_next_scheduled_workout'}), name='next_scheduled_workout'),
    path('workouts/<int:pk>/logs', Workouts.as_view({'get': 'get_workout_logs'}), name='workout_logs'),
    path('workouts/<int:pk>', Workouts.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='retrieve_update_delete_workout'),
    path('workouts', Workouts.as_view({'get': 'list', 'post': 'create'}), name='list_create_workout'),
]
