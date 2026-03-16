from rest_framework import serializers
from .models import TodoItem


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['id', 'title', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']