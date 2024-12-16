from rest_framework import serializers
from .models import Platform, Account, AccountCookie


class AccountCookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCookie
        fields = ['id', 'cookie', 'created_at']

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name', 'description', 'url', 'logo_url']
        read_only_fields = ['id']


class AccountSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer(read_only=True)
    cookies = AccountCookieSerializer(source='accountcookie_set', many=True, read_only=True)  # Liên kết ngược tới AccountCookie
    class Meta:
        model = Account
        fields = ['id', 'platform', 'name', 'is_active', 'rented_by', 'rented_at', 'expires_at', 'cookies']

