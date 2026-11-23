from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, board):
        user = request.user
        if board.owner == user:
            return True
        if request.method == 'DELETE':
            return False
        return board.members.filter(pk=user.pk).exists()