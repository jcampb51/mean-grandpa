# logs.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status
from django.http import HttpResponseForbidden
from grandpaapi.models import Log, Exercise

# Serializers
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'video_link']

class LogSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = Log
        fields = ['id', 'weight', 'reps', 'sets', 'interval', 'exercise']

# ViewSet
class Logs(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        logs = Log.objects.filter(user=request.user)
        serializer = LogSerializer(logs, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            log = Log.objects.get(pk=pk, user=request.user)
            serializer = LogSerializer(log, context={'request': request})
            return Response(serializer.data)
        except Log.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = LogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            log = Log.objects.get(pk=pk, user=request.user)
            serializer = LogSerializer(log, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Log.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            log = Log.objects.get(pk=pk, user=request.user)
            log.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Log.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
