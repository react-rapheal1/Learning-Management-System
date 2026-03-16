from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from core.permissions import IsInstructor, IsCourseOwner
from django.utils import timezone
from drf_spectacular.utils import extend_schema

from .models import Course, Enrollment, Lesson, LessonProgress
from .serializers import (
    InstructorCourseSerializer, LessonSerializer, CourseListSerializer,
    EnrollmentSerializer, LessonProgressSerializer
)
from assignments.serializers import AssignmentSerializer
from schedule.serializers import LiveLessonSerializer



class CreateCourseView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    @extend_schema(
        summary="Create a new course",
        description="Create a new course. Only instructors can create courses.",
        request=InstructorCourseSerializer,
        responses={
            201: InstructorCourseSerializer,
            400: "Bad request - invalid data",
            403: "Forbidden - user is not an instructor"
        }
    )
    def post(self, request):
        serializer = InstructorCourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status = 400)


class InstructorCourseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = InstructorCourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsCourseOwner]

    @extend_schema(
        summary="Get instructor's course details",
        description="Retrieve, update, or delete a course owned by the current instructor.",
        responses={
            200: InstructorCourseSerializer,
            403: "Forbidden - not the course owner",
            404: "Course not found"
        }
    )
    def get_queryset(self):
        return Course.objects.filter(instructor = self.request.user)


class CreateLessonView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    @extend_schema(
        summary="Create a lesson",
        description="Create a new lesson in a course. Only the course instructor can create lessons.",
        request=LessonSerializer,
        responses={
            201: LessonSerializer,
            400: "Bad request - invalid data",
            403: "Forbidden - not the course owner"
        }
    )
    def post(self, request):
        serializer = LessonSerializer(data=request.data)

        if serializer.is_valid():
            course = serializer.validated_data['course']

            if course.instructor != request.user:
                return Response(
                    {"error": "Your do not own this course"},
                    status = 403
                )
            
            serializer.save()
            return Response(serializer.data, status = 201)
        
        return Response(serializer.error, status=400)


class CreateAssignmentView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    @extend_schema(
        summary="Create an assignment",
        description="Create a new assignment for a course. Only the course instructor can create assignments.",
        request=AssignmentSerializer,
        responses={
            201: AssignmentSerializer,
            400: "Bad request - invalid data",
            403: "Forbidden - not the course owner"
        }
    )
    def post(self, request):
        serializer = AssignmentSerializer(data=request.data, context = {'request': request})

        if serializer.is_valid():
            course = serializer.validated_data['course']

            if course.instructor != request.user:
                return Response(
                    {"error": "You do not own this course"},
                    status=403
                )
            
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


class CreateLiveLessonView(APIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    @extend_schema(
        summary="Create a live lesson",
        description="Schedule a new live lesson for a course. Only the course instructor can create live lessons.",
        request=LiveLessonSerializer,
        responses={
            201: LiveLessonSerializer,
            400: "Bad request - invalid data",
            403: "Forbidden - not the course owner"
        }
    )
    def post(self, request):
        serializer = LiveLessonSerializer(data = request.data)

        if serializer.is_valid():
            course = serializer.validated_data['course']

            if course.instructor != request.user:
                return Response(
                    {"eror": "You do not own this course"},
                    status=403
                )
            
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Courses'],
        summary="List all available courses",
        description="Retrieve a list of all courses available for enrollment. Includes course details, instructor information, and enrollment count.",
        responses={
            200: CourseListSerializer(many=True),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get course details",
        description="Retrieve detailed information about a specific course.",
        responses={
            200: CourseListSerializer,
            404: "Course not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Courses'],
        summary="Enroll in a course",
        description="Enroll the current user in the specified course. User must not already be enrolled.",
        responses={
            201: EnrollmentSerializer,
            400: "Already enrolled or bad request",
            404: "Course not found"
        }
    )
    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        # Check if already enrolled
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response({"error": "Already enrolled in this course"}, status=400)

        enrollment = Enrollment.objects.create(user=request.user, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=201)


class StudentEnrollmentsView(ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List user's enrollments",
        description="Retrieve all courses the current user is enrolled in.",
        responses={
            200: EnrollmentSerializer(many=True),
        }
    )
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related('course')


class CourseLessonsView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Lessons'],
        summary="List lessons in a course",
        description="Retrieve all lessons for a specific course. User must be enrolled in the course.",
        responses={
            200: LessonSerializer(many=True),
            403: "Not enrolled in this course"
        }
    )
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        # Check if user is enrolled
        if not Enrollment.objects.filter(user=self.request.user, course_id=course_id).exists():
            return Lesson.objects.none()
        return Lesson.objects.filter(section__course_id=course_id).select_related('section__course')


class MarkLessonCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Mark lesson as completed",
        description="Mark a specific lesson as completed for the current user. User must be enrolled in the course.",
        responses={
            200: LessonProgressSerializer,
            403: "Not enrolled in this course",
            404: "Lesson not found"
        }
    )
    def post(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=404)

        # Check if enrolled in the course
        if not Enrollment.objects.filter(user=request.user, course=lesson.section.course).exists():
            return Response({"error": "Not enrolled in this course"}, status=403)

        progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson,
            defaults={'completed': True, 'completed_at': timezone.now()}
        )

        if not created and not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()

        serializer = LessonProgressSerializer(progress)
        return Response(serializer.data, status=200)


class StudentProgressView(ListAPIView):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get user's lesson progress",
        description="Retrieve the current user's progress across all lessons in enrolled courses.",
        responses={
            200: LessonProgressSerializer(many=True),
        }
    )
    def get_queryset(self):
        return LessonProgress.objects.filter(student=self.request.user).select_related(
            'lesson__section__course'
        )



