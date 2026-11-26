from django.conf import settings
from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('to-do', 'To do'),
        ('in-progress', 'In progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    board = models.ForeignKey('board_app.Board', on_delete=models.CASCADE,
                              related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default='to-do')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES,
                                default='low')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='assigned_tasks')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='reviewing_tasks')
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL,
                                   related_name='created_tasks')

    def __str__(self):
        return self.title