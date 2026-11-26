from rest_framework.permissions import BasePermission


class IsTaskMember(BasePermission):
    def has_object_permission(self, request, view, task):
        user = request.user
        board = task.board
        if request.method == 'DELETE':
            return task.created_by == user or board.owner == user
        if board.owner == user:
            return True
        return board.members.filter(pk=user.pk).exists()
