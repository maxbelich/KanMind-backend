from django.urls import path

from .views import TaskCreateView, TaskDetailView, TaskAssignedToMeView, \
    TaskReviewingView

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/assigned-to-me/', TaskAssignedToMeView.as_view(),
         name='task-assignee'),
    path('tasks/reviewing/', TaskReviewingView.as_view(),
         name='task-reviewing'),
]
