from django.urls import path
from platforms.api import PlatformViewSet, AccountViewSet

from rest_framework.routers import DefaultRouter
from platforms.api import PlatformViewSet, AccountViewSet

router = DefaultRouter()
router.register(r'platforms', PlatformViewSet, basename='platform')
# router.register(r'accounts', AccountViewSet, basename='account')

urlpatterns = router.urls
