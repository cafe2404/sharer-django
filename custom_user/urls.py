from django.urls import path
from .views import auth_views,dashboard_views
from . import api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('api/login/', api.LoginView.as_view(), name='api_login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user-subscription/', api.UserSubscriptionAPIView.as_view(), name='user-subscription'),
    path('settings/', dashboard_views.settings_view, name='settings'),
    path('dashboard/', dashboard_views.dashboard_view, name='dashboard'),
    path('subscriptions/', dashboard_views.subscription_view, name='subscriptions'),
    path('transaction-history/', dashboard_views.transaction_history_view, name='transaction_history'),
    
]
