from rest_framework import serializers

from board_app.models import Board
from user_auth_app.models import User
from user_auth_app.api.serializers import UserShortSerializer


class BoardListSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(),
        write_only=True, required=False,
    )
    owner_id = serializers.IntegerField(read_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'members', 'owner_id', 'member_count',
            'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count',
        ]

    def get_member_count(self, board):
        return board.members.count()

    def get_ticket_count(self, board):
        return 0

    def get_tasks_to_do_count(self, board):
        return 0

    def get_tasks_high_prio_count(self, board):
        return 0

class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(read_only=True)
    members = UserShortSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']

    def get_tasks(self, board):
        return []

class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(),
        write_only=True, required=False,
    )
    owner_data = UserShortSerializer(source='owner', read_only=True)
    members_data = UserShortSerializer(
        source='members', many=True, read_only=True,
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_data', 'members_data']