from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from board_app.models import Board
from .serializers import BoardListSerializer, BoardDetailSerializer,\
    BoardUpdateSerializer
from .permissions import IsBoardOwnerOrMember


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BoardUpdateSerializer
        return BoardDetailSerializer