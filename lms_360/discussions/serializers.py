from rest_framework import serializers
from .models import Discussion, DiscussionReply


class DiscussionReplySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source = 'author.get_full_name', read_only = True)

    class Meta:
        model = DiscussionReply
        fields = ['id', 'author_name', 'content', 'created_at']


class DiscussionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['course', 'category', 'title', 'content']


class DiscussionSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source = 'author.get_full_name', read_only = True)
    likes_count = serializers.IntegerField(read_only = True)
    replies_count = serializers.IntegerField(read_only = True)
    views_count = serializers.IntegerField(read_only = True)

    class Meta:
        model = Discussion
        fields = [
            'id',
            'course',
            'category',
            'title',
            'content',
            'author_name',
            'likes_count',
            'replies_count',
            'views_count',
            'created_at',
        ]
        read_only_fields = ['id', 'author_name', 'likes_count', 'replies_count', 'views_count', 'created_at']