from django.urls import path
from .views import student_assignments, submit_assignment, AssignmentSubmissionsView, GradeSubmissionView

urlpatterns = [
    path('', student_assignments),
    path('<int:assignment_id>/submit/', submit_assignment),
    path('<int:assignment_id>/submissions/', AssignmentSubmissionsView.as_view()),
    path('submissions/<int:pk>/grade/', GradeSubmissionView.as_view()),
]