from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView
from core.permissions import IsInstructor
from drf_spectacular.utils import extend_schema

from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSubmissionSerializer
from django.views.decorators.http import require_POST


@login_required
def student_assignments(request):
    user = request.user

    assignments = Assignment.objects.filter(
        course__enrollments__student = user
    ).select_related('course', 'lesson')

    data = []

    for assignment in assignments:
        submission = AssignmentSubmission.objects.filter(
            assignment = assignment, student=user
        ).first()

        if submission:
            status = submission.status
        else:
            status = 'pending'

        data.append({
            "id": assignment.id,
            "title": assignment.title,
            "course": assignment.course.title,
            "lesson": assignment.lesson.title if assignment.lesson else None,
            "due_date": assignment.due_date,
            "status": status,
            "submitted": submission is not None,
        })

    return JsonResponse(data, safe=False)


@require_POST
@login_required
def submit_assignment(request, assignment_id):
    user = request.user
    file = request.FILES.get('file')

    assignment = Assignment.objects.get(id = assignment_id)
    
    submission, created = AssignmentSubmission.objects.get_or_create(
        assignment = assignment,
        student = user,
        defaults={'file': file}
    )

    if not created:
        submission.file = file

    submission.update_status()

    return JsonResponse({"message": "Assignment submitted successfully"})


class AssignmentSubmissionsView(ListAPIView):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    @extend_schema(
        tags=['Assignments'],
        summary="List assignment submissions",
        description="Retrieve all submissions for a specific assignment. Only the course instructor can view submissions.",
        responses={
            200: AssignmentSubmissionSerializer(many=True),
            403: "Forbidden - not the course instructor"
        }
    )
    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        assignment = Assignment.objects.get(id=assignment_id)

        # Check if user is the instructor
        if assignment.course.instructor != self.request.user:
            return AssignmentSubmission.objects.none()

        return AssignmentSubmission.objects.filter(assignment=assignment).select_related(
            'assignment__course', 'student'
        )


class GradeSubmissionView(UpdateAPIView):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
    queryset = AssignmentSubmission.objects.all()

    @extend_schema(
        tags=['Assignments'],
        summary="Grade an assignment submission",
        description="Update the grade for a specific assignment submission. Only the course instructor can grade submissions.",
        request=AssignmentSubmissionSerializer,
        responses={
            200: AssignmentSubmissionSerializer,
            403: "Forbidden - not the course instructor",
            404: "Submission not found"
        }
    )
    def perform_update(self, serializer):
        # Check if user is the instructor
        if serializer.instance.assignment.course.instructor != self.request.user:
            raise PermissionError("Only the course instructor can grade submissions.")

        serializer.save()
