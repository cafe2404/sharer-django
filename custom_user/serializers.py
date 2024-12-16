from rest_framework import serializers
from platforms.serializers import AccountSerializer
from subscriptions.serializers import SubscriptionPlanSerializer
from .models import CustomUser as User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSubscriptionSerializer(serializers.ModelSerializer):
    subscription_plan = SubscriptionPlanSerializer(source='get_current_package.subscription_plan', read_only=True)
    accounts = AccountSerializer(many=True, read_only=True)  # Serialize cả tài khoản thuộc gói và không thuộc gói

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'subscription_plan', 'accounts']

