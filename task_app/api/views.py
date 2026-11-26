from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import TaskSerializer, TaskUpdateSerializer
from task_app.models import Task
from .permissions import IsTaskMember


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsTaskMember]
    http_method_names = ['patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return TaskUpdateSerializer
        return TaskSerializer
