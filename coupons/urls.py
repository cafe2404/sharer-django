from . import api
from django.urls import path

urlpatterns = [
    path('use/', api.UseCouponAPIView.as_view(), name='use-coupon'),
]
