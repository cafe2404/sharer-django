from rest_framework import serializers
from .models import SubscriptionPlan, PackageToken, SubscriptionPlanDuration

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class PackageTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageToken
        fields = ['id', 'token', 'created_at', 'expires_at', 'user']

class SubscriptionPlanDurationSerializer(serializers.ModelSerializer):
    subscription_plan = SubscriptionPlanSerializer()
    class Meta:
        model = SubscriptionPlanDuration
        fields = '__all__'
