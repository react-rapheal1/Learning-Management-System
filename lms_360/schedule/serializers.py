from rest_framework import serializers
from .models import LiveLesson


class LiveLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = LiveLesson
        fields = [
            'id',
            'course',
            'title',
            'instructor',
            'start_time',
            'duration_minutes',
            'meeting_link',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_course(self, value):
        request = self.context.get('request')

        if value.instructor != request.user:
            raise serializers.ValidationError(
                "You can only create live lessons for your own courses."
            )

        return value


