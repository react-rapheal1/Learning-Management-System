from django.urls import path
from .views import (
    CreateCourseView, InstructorCourseDetailView, CreateLessonView,
    CreateAssignmentView, CreateLiveLessonView, CourseListView,
    CourseDetailView, EnrollCourseView, StudentEnrollmentsView,
    CourseLessonsView, MarkLessonCompleteView, StudentProgressView
)

urlpatterns = [

    # Course Management
    path('instructor/courses/create/', CreateCourseView.as_view()),
    path('instructor/courses/<int:pk>/', InstructorCourseDetailView.as_view()),

    # Lessons
    path(
        'instructor/courses/<int:course_id>/lessons/create/',
        CreateLessonView.as_view()
    ),

    # Assignments
    path(
        'instructor/courses/<int:course_id>/assignments/create/',
        CreateAssignmentView.as_view()
    ),

    # Live Lessons
    path(
        'instructor/courses/<int:course_id>/live-lessons/create/',
        CreateLiveLessonView.as_view()
    ),

    # Student endpoints
    path('list/', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('<int:course_id>/enroll/', EnrollCourseView.as_view()),
    path('my-enrollments/', StudentEnrollmentsView.as_view()),
    path('<int:course_id>/lessons/', CourseLessonsView.as_view()),
    path('lessons/<int:lesson_id>/complete/', MarkLessonCompleteView.as_view()),
    path('my-progress/', StudentProgressView.as_view()),
]