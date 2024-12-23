from django.urls import path
from . import views

urlpatterns = [
    path('<int:cookie_id>/', views.reverse_proxy, name='reverse_proxy_spy'),
]
