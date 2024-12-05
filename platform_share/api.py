from rest_framework import viewsets, permissions
from .models import Platform, PlatformAccount
from .serializers import PlatformSerializer, PlatformAccountSerializer
from django.db import models

class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [permissions.IsAuthenticated]

class PlatformAccountViewSet(viewsets.ModelViewSet):
    serializer_class = PlatformAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        # Tài khoản mà user có quyền truy cập (trực tiếp hoặc qua nhóm)
        return PlatformAccount.objects.filter(
            models.Q(users=user) | 
            models.Q(groups__users=user)
        ).distinct()
