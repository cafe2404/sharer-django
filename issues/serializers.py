from rest_framework import serializers
from .models import Issue

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'content', 'image', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']  # Các trường chỉ đọc
