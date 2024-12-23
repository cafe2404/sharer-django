
from django.shortcuts import get_object_or_404
from .models import PaymentSetting
from subscriptions.models import SubscriptionPlanDuration
import json
from coupons.models import Coupon, UserCoupon



def apply_coupon_to_order(order, user, coupon_code):
    try:
        coupon = Coupon.get_valid_coupon(coupon_code)
        if not coupon:
            return {"success": False, "message": f"Mã giảm giá {coupon_code} không hợp lệ."}

        if coupon.usage_limit and coupon.times_used >= coupon.usage_limit:
            return {"success": False, "message": f"Mã giảm giá {coupon_code} đã hết lượt sử dụng."}
        if order.coupons.filter(code=coupon.code).exists():
            return {"success": False, "message": f"Mã giảm giá {coupon_code} đã được dùng rồi."}
        if UserCoupon.objects.filter(user=user, coupon=coupon, is_used=True).exists():
            return {"success": False, "message": f"Mã giảm giá {coupon_code} đã được sử dụng."}

        order.coupons.add(coupon)
        order.save()
        UserCoupon.objects.create(user=user, coupon=coupon, is_used=False)
        return {"success": True, "message": f"Mã giảm giá {coupon_code} đã được áp dụng!", "order": order}
    except Coupon.DoesNotExist:
        return {"success": False, "message": f"Mã giảm giá {coupon_code} không hợp lệ."}



def update_order_duration(order, duration_id):
    """
    Cập nhật thời hạn cho đơn hàng.
    """
    duration = get_object_or_404(SubscriptionPlanDuration, id=duration_id)
    if duration.subscription_plan != order.subscription_plan:
        return {"success": False, "message": "Thời hạn không hợp lệ cho gói đăng ký hiện tại."}

    order.subscription_duration = duration
    order.save()
    return {"success": True, "message": "Thời hạn đã được cập nhật!", "order": order, "duration": duration.duration}



def create_qr_code(bank_info:PaymentSetting, amount, order_id):
    """
    Tạo mã QR code cho đơn hàng.
    """
    qr_code = f'https://api.vietqr.io/image/{bank_info.bank_code}-{bank_info.account_number}-QKZsa4f.jpg?amount={amount}&addInfo={order_id}'
    return qr_code