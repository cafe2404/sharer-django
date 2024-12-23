from .models import PackageToken, SubscriptionPlan,SubscriptionDurationFilter,SubscriptionPlanDuration
from django.utils.timezone import now

def subscriptions_context(request):
    subscriptions = SubscriptionPlan.objects.all().order_by('level')
    subscription_tab_filters = SubscriptionDurationFilter.objects.all()
    subscription_durations = SubscriptionPlanDuration.objects.all()
    # Lấy gói hiện tại mà người dùng đang sử dụng (nếu có)
    if request.user.is_authenticated:
        current_token = PackageToken.objects.filter(user=request.user, is_active=True, expires_at__gt=now()).first()
    else:
        current_token = None
    return {
        'subscriptions':subscriptions,
        'subscription_durations':subscription_durations,
        'current_subscription_duration': current_token.account_group.subscription_duration if current_token else None,
        'current_account_group':current_token.account_group if current_token else None,
        'current_token':current_token,
        'subscription_tab_filters':subscription_tab_filters,
    }