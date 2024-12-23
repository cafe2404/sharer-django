from django.urls import path
from . import views
from .api import PlatformViewSet, PlatformAccountViewSet

urlpatterns = [
    path('platform_accounts/', views.platform_accounts, name='platform_accounts'),
    path('platform_account_detail/<account_id>/', views.platform_account_detail, name='platform_account_detail'),
    path('api/platforms/', PlatformViewSet.as_view({'get': 'list', 'post': 'create'}), name='platform-list'),
    path('api/platforms/<int:pk>/', PlatformViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='platform-detail'),
    path('api/platform-accounts/', PlatformAccountViewSet.as_view({'get': 'list', 'post': 'create'}), name='platform-account-list'),
    path('api/platform-accounts/<int:pk>/', PlatformAccountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='platform-account-detail'),
    # path('<path:path>', views.reverse_proxy_semrush, name='reverse_proxy_semrush'),
    # path('', views.reverse_proxy_semrush, name='reverse_proxy_semrush'),
]
