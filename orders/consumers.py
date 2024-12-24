# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from orders.models import Order
from asgiref.sync import sync_to_async  # Import sync_to_async để gọi các hàm đồng bộ

class PaymentStatusConsumer(AsyncWebsocketConsumer):
    # Kết nối WebSocket
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f'order_{self.order_id}'
        print(self.group_name)
        await self.channel_layer.group_add(
            self.group_name,  
            self.channel_name  
        )
        await self.accept()
    async def disconnect(self, close_code):
        await self.cancel_order_if_needed(self.order_id)
        
        await self.channel_layer.group_discard(
            self.group_name,  
            self.channel_name 
        )
    async def payment_status_message(self, event):
        message = event['message']
        success = event.get('success', 0)  # Default to 0 if success is not included
        await self.send(text_data=json.dumps({
            'message': message,
            'success' : success
        }))

    @sync_to_async
    def cancel_order_if_needed(self, order_id):
        try:
            order = Order.objects.get(order_id=order_id)

            # Kiểm tra nếu đơn hàng chưa được thanh toán và chưa hoàn tất
            if  order.status != 'paid':
                # Huỷ đơn hàng
                order.status = 'failed'
                order.save()
                print(f"Đơn hàng {order_id} đã bị huỷ.")
        except Order.DoesNotExist:
            print(f"Đơn hàng {order_id} không tồn tại.")