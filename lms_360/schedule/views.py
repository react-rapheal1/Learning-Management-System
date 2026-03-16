from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from courses.models import Enrollment
from drf_spectacular.utils import extend_schema

from .models import LiveLesson
from .serializers import LiveLessonSerializer


class LiveLessonListView(ListAPIView):
    serializer_class = LiveLessonSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Schedule'],
        summary="List enrolled live lessons",
        description="Retrieve all live lessons for courses the user is enrolled in.",
        responses={
            200: LiveLessonSerializer(many=True),
        }
    )
    def get_queryset(self):
        # Return live lessons for courses the user is enrolled in
        enrolled_course_ids = Enrollment.objects.filter(
            user=self.request.user
        ).values_list('course_id', flat=True)

        return LiveLesson.objects.filter(
            course_id__in=enrolled_course_ids
        ).select_related('course', 'instructor').order_by('start_time')


class InstructorLiveLessonListView(ListAPIView):
    serializer_class = LiveLessonSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Schedule'],
        summary="List instructor's live lessons",
        description="Retrieve all live lessons created by the current instructor.",
        responses={
            200: LiveLessonSerializer(many=True),
        }
    )
    def get_queryset(self):
        # Return live lessons created by the instructor
        return LiveLesson.objects.filter(
            instructor=self.request.user
        ).select_related('course').order_by('start_time')
