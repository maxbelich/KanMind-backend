from rest_framework import generics

from .serializers import TaskSerializer


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)