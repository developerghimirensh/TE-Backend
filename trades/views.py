from rest_framework import generics, permissions

from .models import Trade
from .serializers import TradeSerializer


class TradeListCreateView(generics.ListCreateAPIView):
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class TradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(
            user=self.request.user
        )