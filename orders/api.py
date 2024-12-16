# API to create an order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Order
from subscriptions.models import SubscriptionPlan, SubscriptionPlanDuration


class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription_plan_id = request.data.get('subscription_plan_id')
        subscription_plan_duration_id = request.data.get('subscription_plan_duration_id')

        # Kiểm tra input
        if not subscription_plan_id:
            return Response(
                {"error": "Subscription plan ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Lấy thông tin kế hoạch đăng ký
        subscription_plan = get_object_or_404(SubscriptionPlan, id=subscription_plan_id)

        # Lấy thời hạn gói mặc định nếu không được cung cấp
        if subscription_plan_duration_id:
            subscription_duration = get_object_or_404(
                SubscriptionPlanDuration, id=subscription_plan_duration_id
            )
        else:
            subscription_duration = (
                SubscriptionPlanDuration.objects.filter(subscription_plan=subscription_plan)
                .order_by('duration')  # Lấy thời hạn thấp nhất
                .first()
            )
            if not subscription_duration:
                return Response(
                    {"error": "No duration is available for the selected subscription plan."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            # Tạo Order mới
            order = Order(
                user=request.user,
                subscription_plan=subscription_plan,
                subscription_duration=subscription_duration,
                status='pending'  # Trạng thái mặc định
            )
            order.save()  # Lưu lần đầu để tạo ID

            # Tạo nội dung QR code
            qr_content = f"Chuyển khoản nội dung: {order.order_id} - Số tiền: {order.amount}"

            return Response(
                {
                    "message": "Order created successfully.",
                    "order_id": order.order_id,
                    "amount": order.amount,
                    "qr_content": qr_content,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
