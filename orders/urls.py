from django.urls import path

from . import views, api , webhooks
urlpatterns = [
    path("orders/payment-success/",views.payment_success , name="payment_success"),
    path('orders/<order_id>/', views.order, name='order'),
    path('api/orders/create/',api.CreateOrderAPIView.as_view(),name='create_order'),
    path('webhooks/se-pay/',webhooks.PaymentWebhookView.as_view(),name='sepay-webhook'),
]
