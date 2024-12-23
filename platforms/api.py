from rest_framework import viewsets, permissions,status
from .models import Platform, Account
from .serializers import PlatformSerializer, AccountSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import pyotp

class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [permissions.IsAuthenticated]

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Account.objects.all()
    
    @action(detail=True, methods=['get'], url_path='two_factor_auth')
    def generate_otp(self, request, pk=None):
        """
        Trả về mã OTP cho tài khoản.
        """
        account = self.get_object()
        if not account.two_factor_auth:
            return Response({"error": "Tài khoản này chưa được cấu hình mã 2FA."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Sử dụng PyOTP để tạo mã OTP
        totp = pyotp.TOTP(account.two_factor_auth)
        otp_code = totp.now()

        return Response({"otp_code": otp_code, "account_id": account.id, "name": account.name})