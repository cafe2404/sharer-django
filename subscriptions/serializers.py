from rest_framework import serializers
from .models import SubscriptionPlan, PackageToken, SubscriptionPlanDuration
from sharer.templatetags.custom_filters import parse_currency

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
    formatted_price = serializers.SerializerMethodField()
    class Meta:
        model = SubscriptionPlanDuration
        fields = '__all__'
        
    def get_formatted_price(self, obj):
        """
        Hàm này sẽ chuyển giá trị price thành định dạng tiền tệ, ví dụ: "299,000 đ".
        """
        return parse_currency(obj.price)