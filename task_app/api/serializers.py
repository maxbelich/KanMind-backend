from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from board_app.models import Board
from task_app.models import Task
from user_auth_app.models import User
from user_auth_app.api.serializers import UserShortSerializer


def is_board_member(board, user):
    if board.owner == user:
        return True
    if board.members.filter(pk=user.pk).exists():
        return True
    return False


class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False,
        source='assignee', write_only=True, allow_null=True)
    assignee = UserShortSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False,
        source='reviewer', write_only=True, allow_null=True)
    reviewer = UserShortSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status',
            'priority', 'assignee', 'assignee_id',
            'reviewer', 'reviewer_id', 'due_date', 'comments_count',
        ]

    def validate(self, attrs):
        board = attrs['board']
        user = self.context['request'].user
        if not is_board_member(board, user):
            raise PermissionDenied("You're not a member of this board. "
                                   "Ask the Owner to assign you.")
        for name in ('assignee', 'reviewer'):
            person = attrs.get(name)
            if person is not None and not is_board_member(board, person):
                attrs[name] = None
        return attrs

    def get_comments_count(self, task):
        return 0