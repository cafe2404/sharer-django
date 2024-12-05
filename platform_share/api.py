from rest_framework import viewsets, permissions
from .models import Platform, PlatformAccount
from .serializers import PlatformSerializer, PlatformAccountSerializer

class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [permissions.IsAuthenticated]

class PlatformAccountViewSet(viewsets.ModelViewSet):
    serializer_class = PlatformAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # Only return platform accounts owned by the current user
        return PlatformAccount.objects.filter(user=self.request.user)
