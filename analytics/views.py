from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .calculations import build_analytics
from .serializers import AnalyticsSerializer


class AnalyticsView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        analytics = build_analytics(
            request.user
        )

        serializer = AnalyticsSerializer(
            analytics
        )

        return Response(
            serializer.data
        )