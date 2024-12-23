from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Issue
from .serializers import IssueSerializer

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by('-created_at')  # Sắp xếp theo ngày tạo mới nhất
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]  # Chỉ cho phép người dùng đã đăng nhập

    def perform_create(self, serializer):
        """
        Ghi đè để tự động gán người dùng hiện tại cho `user`.
        """
        serializer.save(user=self.request.user)
