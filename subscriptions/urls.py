from django.urls import path
from . import api
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', api.SubscriptionAPIView.as_view(), name='register-subscription'),
]
