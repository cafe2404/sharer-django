from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Package, PackageToken
from django.utils.timezone import  now
from dateutil.relativedelta import relativedelta
from coupons.models import UserCoupon
from orders.models import Order
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SubscriptionAPIView(APIView):
    """
    API để tạo hoặc nâng cấp token gói đăng ký.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_id = request.data.get('order_id')

        # Kiểm tra và lấy Order
        try:
            order = Order.objects.get(order_id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({"error": "Order không tồn tại hoặc không thuộc về bạn."}, status=status.HTTP_404_NOT_FOUND)

        if not order.subscription_plan or not order.subscription_duration:
            return Response({"error": "Đơn hàng không có gói đăng ký hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem người dùng đã có token chưa
        existing_token = PackageToken.objects.filter(user=user, is_active=True).first()

        if existing_token:
            # Nếu người dùng đã có token, tiến hành nâng cấp
            try:
                expires_at = now() + relativedelta(months=order.subscription_duration.duration)
                existing_token.package = Package.find_available_package(order.subscription_duration)
                existing_token.expires_at = expires_at
                existing_token.save()
                message = "Token đã được nâng cấp thành công."
                token = existing_token
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Nếu người dùng chưa có token, tạo token mới
            try:
                new_token = PackageToken.create_from_order(order)
                message = "Token mới đã được tạo thành công."
                token = new_token
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                  # Đánh dấu coupon đã sử dụng
        self.mark_coupon_as_used(order,token)
        order.is_used = True
        order.save()
        # Phản hồi kết quả
        response_data = {
            "message": message,
            "status": "success",
            "token": token.token,
            "expires_at": token.expires_at,
            "package": token.package.name,
            "is_upgraded": bool(existing_token),
        }
        return Response(response_data, status=status.HTTP_200_OK)
    @staticmethod
    def mark_coupon_as_used(order:Optional[Order],token:Optional[PackageToken]):
        """
        Đánh dấu các mã giảm giá trong đơn hàng là đã sử dụng khi thanh toán thành công,
        và xử lý thêm ngày sử dụng nếu có.
        """
        try:
            for coupon in order.coupons.all():
                # Cập nhật trạng thái `UserCoupon`
                user_coupon = UserCoupon.objects.filter(user=order.user, coupon=coupon, is_used=False).first()
                if user_coupon:
                    user_coupon.is_used = True
                    user_coupon.save()

                # Tăng số lần sử dụng mã
                coupon.times_used += 1
                coupon.save()
                if coupon.additional_days:
                    token.expires_at += relativedelta(days=coupon.additional_days)
                    token.save()
        except Exception as e:
            logger.error(f"Lỗi khi đánh dấu mã giảm giá đã sử dụng: {str(e)}")