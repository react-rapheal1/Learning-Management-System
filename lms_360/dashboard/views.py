from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from courses.models import Course
from core.permissions import IsEnrolledInCourse
from drf_spectacular.utils import extend_schema

from .models import TodoItem
from .serializers import TodoSerializer
from .services import (
    get_recent_course_with_progress,
    get_learning_hours,
    get_performance,
    get_todos,
    get_recent_enrolled_classes,
    get_upcoming_lessons,
    start_learning_session,
    end_learning_session,
)


@login_required
def dashboard_summary(request):
    user = request.user

    data = {
        "student_name": user.first_name,
        "recent_course": get_recent_course_with_progress(user),
        "learning_hours": get_learning_hours(user),
        "performance": get_performance,
        "todos": get_todos(user),
        "recent_classes": get_recent_enrolled_classes(user),
        "upcoming_lessons": get_upcoming_lessons(user),
    }

    return JsonResponse(data)

class StartLearningSessionView(APIView):
    permission_classes = [IsAuthenticated, IsEnrolledInCourse]

    @extend_schema(
        summary="Start learning session",
        description="Start a learning session for a specific course. User must be enrolled in the course.",
        responses={
            200: {"message": "Session started"},
            403: "Forbidden - not enrolled in course",
            404: "Course not found"
        }
    )
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        start_learning_session(request.user, course)

        return Response({"message": "Session started"})


class EndLearningSessionView(APIView):
    permission_classes = [IsAuthenticated, IsEnrolledInCourse]

    @extend_schema(
        summary="End learning session",
        description="End the current learning session for a specific course. User must be enrolled in the course.",
        responses={
            200: {"message": "Session ended"},
            403: "Forbidden - not enrolled in course",
            404: "Course not found"
        }
    )
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        end_learning_session(request.user, course)

        return Response({"message": "Session ended"})


class TodoListView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Dashboard'],
        summary="List and create todos",
        description="Retrieve all todos for the current user or create a new todo.",
        responses={
            200: TodoSerializer(many=True),
            201: TodoSerializer,
        }
    )
    def get_queryset(self):
        return TodoItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Manage specific todo",
        description="Retrieve, update, or delete a specific todo item. Users can only manage their own todos.",
        responses={
            200: TodoSerializer,
            403: "Forbidden - not the todo owner",
            404: "Todo not found"
        }
    )
    def get_queryset(self):
        return TodoItem.objects.filter(user=self.request.user)



