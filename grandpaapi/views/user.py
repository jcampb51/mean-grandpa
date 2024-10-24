from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from grandpaapi.models import Profile, Picture, Post


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['dob', 'photo_access', 'post_access', 'profile_access', 'kudos_access', 'admin_lock', 'is_minor', 'paid_client', 'picture']


# Picture Serializer
class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'post_id', 'img_source', 'upload_date']


# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user_id', 'video_link', 'title', 'body']


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users, including related Profile, Picture, and Post data"""

    profile = ProfileSerializer(read_only=True)  # Assuming a one-to-one relationship
    pictures = PictureSerializer(many=True, read_only=True)  # Assuming one-to-many
    posts = PostSerializer(many=True, read_only=True)  # Assuming one-to-many

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'profile', 'pictures', 'posts')
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only


class Users(ViewSet):
    """Users for Grandpa
    Purpose: Allow a user to communicate with the Grandpa database to GET PUT POST and DELETE Users.
    Methods: GET PUT(id) POST
    """

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user
        Purpose: Retrieve a single user with their profile, pictures, and posts
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to list users along with their profile, pictures, and posts"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
