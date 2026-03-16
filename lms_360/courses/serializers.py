from rest_framework import serializers
from .models import Course, Lesson, Enrollment, LessonProgress


class InstructorCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'title', 'description']


class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='section.course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'duration_minutes', 'is_preview', 'order', 'course_title']


class CourseListSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    enrolled_students_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'price', 'language',
            'difficulty', 'duration_hours', 'thumbnail', 'intro_video_url',
            'instructor_name', 'created_at', 'enrolled_students_count'
        ]

    def get_enrolled_students_count(self, obj):
        return obj.enrollments.count()


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'course_title', 'student_name', 'enrolled_at']
        read_only_fields = ['id', 'enrolled_at']


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    course_title = serializers.CharField(source='lesson.section.course.title', read_only=True)

    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'lesson_title', 'course_title', 'completed', 'completed_at']
        read_only_fields = ['id', 'completed_at']



