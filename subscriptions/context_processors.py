from .models import PackageToken, SubscriptionPlan, Package
from django.utils.timezone import now

def subscriptions_context(request):
    subscriptions = SubscriptionPlan.objects.all()
    # Lấy gói hiện tại mà người dùng đang sử dụng (nếu có)
    if request.user.is_authenticated:
        current_token = PackageToken.objects.filter(user=request.user, is_active=True, expires_at__gt=now()).first()
    else:
        current_token = None
        
    return {
        'subscriptions':subscriptions,
        'current_subscription': current_token.package.subscription_plan if current_token else None,
        'current_package':current_token.package if current_token else None,
        'current_token':current_token,
    }