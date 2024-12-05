from rest_framework import serializers
from .models import Platform, PlatformAccount


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name', 'description', 'url', 'logo_url']
        read_only_fields = ['id']


class PlatformAccountSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer(read_only=True)
    platform_id = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(),
        source='platform',
        write_only=True
    )
    time_left = serializers.SerializerMethodField()
    class Meta:
        model = PlatformAccount
        fields = ['id', 'platform', 'platform_id', 'username', 'password', 'cookie', 
                 'created_at', 'updated_at', 'expired_at','time_left','login']
        
    def get_time_left(self, obj):
        return obj.time_left()

