from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import timedelta
from .models import Coupon, UserCoupon
from subscriptions.models import PackageToken  # Dùng để thêm ngày vào gói
from django.db import transaction

class UseCouponAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        code = request.data.get('code')  # Lấy mã giảm giá
        user = request.user

        if not code:
            return Response({"error": "Coupon code is required."}, status=400)
        try:
            # Kiểm tra mã giảm giá
            coupon = Coupon.objects.get(code=code)
            if not coupon.is_valid():
                return Response({"error": "Coupon is expired or inactive."}, status=400)

            # Kiểm tra số lần sử dụng
            user_coupon = UserCoupon.objects.filter(user=user, coupon=coupon, is_used=False).first()
            if user_coupon:
                return Response({"error": "You have already used this coupon."}, status=400)

            # Lấy token hiện tại của người dùng
            token = PackageToken.objects.filter(user=user, is_active=True).first()

            if not token:
                return Response({"error": "You don't have an active subscription to apply this coupon."}, status=400)

            # Áp dụng giảm giá hoặc thêm ngày
            with transaction.atomic():
                if coupon.discount_amount:
                    # Cập nhật giá trị giảm
                    token.package.discount = (token.package.discount or 0) + coupon.discount_amount
                if coupon.additional_days:
                    # Thêm ngày vào thời hạn
                    token.expires_at += timedelta(days=coupon.additional_days)

                token.save()

                # Đánh dấu coupon đã sử dụng
                UserCoupon.objects.create(user=user, coupon=coupon, is_used=True)

            return Response({
                "message": "Coupon applied successfully.",
                "token_expiration": token.expires_at,
            }, status=200)

        except Coupon.DoesNotExist:
            return Response({"error": "Invalid coupon code."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
