from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import LoginSerializer, UserSubscriptionSerializer
from subscriptions.models import PackageToken
from platforms.models import Account
from platforms.serializers import AccountSerializer,AccountGroupSerializer


class LoginView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response({
                    "message": "Đăng nhập thành công",
                    "access": access_token,
                    "user": username,
                    "refresh": refresh_token
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Tên đăng nhập hoặc mật khẩu không chính xác"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API cho đăng xuất
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            # Lấy refresh token từ header Authorization
            refresh_token = request.data.get('refresh_token')
            
            # Nếu không có refresh token trong request
            if not refresh_token:
                return Response({"detail": "Refresh token missing"}, status=400)

            # Giải mã token và xóa nó
            token = RefreshToken(refresh_token)
            token.blacklist()  # Đánh dấu token này là không hợp lệ nữa
            
            return Response({"detail": "Logged out successfully"}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

class UserSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user

        # Kiểm tra người dùng có gói đăng ký hay không
        package_token = PackageToken.objects.filter(user=user, is_active=True).first()

        # Lấy tài khoản của người dùng (cả tài khoản thuộc gói và không thuộc gói)
        accounts = Account.objects.filter(rented_by=user)
        # Serialize thông tin người dùng, gói đăng ký và tài khoản của họ
        user_subscription_serializer = UserSubscriptionSerializer(user)
        account_group_serializer = AccountGroupSerializer(package_token.account_group)
        account_serializer = AccountSerializer(accounts, many=True)
        return Response({
            "user": user_subscription_serializer.data,
            "account_group": account_group_serializer.data,
            "accounts": account_serializer.data  # Bao gồm cả tài khoản ngoài gói
        }, status=status.HTTP_200_OK)

