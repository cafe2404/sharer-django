from rest_framework import serializers
from .models import SubscriptionPlan, PackageToken, Package
from platforms.serializers import AccountSerializer

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class PackageTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageToken
        fields = ['id', 'token', 'created_at', 'expires_at', 'user']

class PackageSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True)
    subscription_plan = SubscriptionPlanSerializer()
    class Meta:
        model = Package
        fields = ['id', 'subscription_plan', 'accounts']
