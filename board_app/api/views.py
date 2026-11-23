from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from board_app.models import Board
from .serializers import BoardListSerializer, BoardDetailSerializer
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

class BoardDetailView(generics.RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]