# webhook.py
from .models import Order
from  rest_framework.views import APIView
from rest_framework import status,response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class PaymentWebhookView(APIView):
    def post(self, request):
        # Lấy dữ liệu JSON từ cổng thanh toán
        data = request.data
        print(data)
        # Xử lý số tiền thanh toán và chuyển thành Decimal
        transfer_amount = data.get('transferAmount')

        if transfer_amount is None:
            return response.Response({"error": "Invalid data, missing transferAmount."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem có order_id trong nội dung chuyển tiền không
        content = data.get('content')
        if not content:
            print("Order ID not found in the payment content.")
            return response.Response({"error": "Missing content in the payment."}, status=status.HTTP_400_BAD_REQUEST)

        # Tìm order_id trong nội dung chuyển tiền
        order_id = content
        if not order_id:
            print("Order ID not found in the payment content.")
            return response.Response({"error": "Order ID not found in the payment content."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(order_id=order_id, status='pending')
            # if float(order.amount) != float(transfer_amount):
            #     return response.Response({"error": "Amount mismatch."}, status=status.HTTP_400_BAD_REQUEST)
            order.status = 'paid'
            order.transfer_amount = transfer_amount
            order.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'order_{order_id}',  # Tên nhóm
                {
                    'type': 'payment_status_message',
                    'message': f"Payment for order {order_id} successful.",
                    'success':1
                }
            )
            return response.Response({
                "message": "Payment successful.",
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            print("Order not found.")
            return response.Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return response.Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)