from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Order,PaymentSetting
from subscriptions.models import SubscriptionPlanDuration
import json
from sharer.templatetags.custom_filters import parse_currency
from coupons.models import Coupon, UserCoupon
# Create your views here.
def order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user, status='pending')
    public_coupon = Coupon.get_latest_valid_public_coupon()
    bank_info = PaymentSetting.objects.filter(is_active=True).first()
    if request.method == 'POST':
        data = json.loads(request.body)
        duration_id = data.get('duration_id')
        coupon_code = data.get('coupon_code')
        # Xử lý mã giảm giá
        if coupon_code:
            coupon_response = apply_coupon_to_order(order, request.user, coupon_code)
            if coupon_response["success"]:
                return JsonResponse({
                    "success": True,
                    "message": coupon_response["message"],
                    "price": parse_currency(order.amount),
                    "qr_code": create_qr_code(bank_info, order.amount, order.order_id)
                })
            return JsonResponse({"success": False, "message": coupon_response["message"]})
        # Xử lý cập nhật thời hạn
        if duration_id:
            duration_response = update_order_duration(order, duration_id)
            if duration_response["success"]:
                return JsonResponse({
                    'success': True,
                    'message': duration_response["message"],
                    'price': parse_currency(order.amount),
                    'qr_code': create_qr_code(bank_info, order.amount, order.order_id),
                    'duration': duration_response["duration"]
                })
            return JsonResponse({"success": False, "message": duration_response["message"]})
        return JsonResponse({"success": False, "message": "Invalid request."})
    elif request.method == 'DELETE':
        # Xử lý xóa mã giảm giá
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code')

        if not coupon_code:
            return JsonResponse({"success": False, "message": "Coupon code is required."})

        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon not in order.coupons.all():
                return JsonResponse({"success": False, "message": "Coupon not found in the order."})

            # Xóa coupon khỏi đơn hàng
            order.coupons.remove(coupon)
            order.save()

            return JsonResponse({
                "success": True,
                "message": "Đã xóa counpon khỏi đơn hàng.",
                "price": parse_currency(order.amount),
                "qr_code": create_qr_code(bank_info, order.amount, order.order_id)
            })
            
        except Coupon.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid coupon code."})
    # Render thông tin đơn hàng
    durations = SubscriptionPlanDuration.objects.filter(subscription_plan=order.subscription_plan)
    print(public_coupon)
    return render(request, 'pages/order.html', {
        "order": order,
        "qr_code": create_qr_code(bank_info, order.amount, order.order_id),
        "durations": durations,
        "public_coupon": public_coupon
    })

def payment_success(request):
    return render(request, 'pages/payment_success.html')

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