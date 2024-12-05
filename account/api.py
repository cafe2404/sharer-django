from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import LoginSerializer

class LoginView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # Generate token pair (access and refresh token)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Return tokens in response
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
        # Hủy token khi người dùng đăng xuất
        return Response({"detail": "Logged out successfully"})

