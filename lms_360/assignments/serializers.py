from rest_framework import serializers
from .models import Assignment, AssignmentSubmission


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = [
            'id',
            'title',
            'course',
            'lesson',
            'due_date',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_course(self, value):
        request = self.context.get('request')

        if value.instructor != request.user:
            raise serializers.ValidationError(
                "You can only create assignments for your own courses."
            )
        return value


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    course_title = serializers.CharField(source='assignment.course.title', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'assignment_title', 'course_title', 'student', 'student_name',
            'file', 'status', 'grade', 'submitted_at'
        ]
        read_only_fields = ['id', 'submitted_at', 'status']

    def update(self, instance, validated_data):
        # Only instructors can grade
        request = self.context.get('request')
        if instance.assignment.course.instructor != request.user:
            raise serializers.ValidationError("Only the course instructor can grade submissions.")

        return super().update(instance, validated_data)


