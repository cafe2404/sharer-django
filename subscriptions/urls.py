from django.urls import path
from . import api
from . import views

urlpatterns = [
    path('register/', api.SubscriptionAPIView.as_view(), name='register_subscription'),
    path('trial/', api.TrialSubscriptionAPIView.as_view(), name='trial_subscription'),
    path('embed/', views.subscriptions_iframes, name='subscriptions_iframes'),
]
