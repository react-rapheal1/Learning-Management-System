from django.db import models
from django.conf import settings
from courses.models import Course, Lesson

User = settings.AUTH_USER_MODEL


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course, on_delete = models.CASCADE, related_name='assignments'
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, null=True, blank=True
    )

    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('progress', 'In Progress'),
    ('done', 'Done'),
    )

    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='submissions'
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignment_submissions'
    )

    file = models.FileField(upload_to='assignments/')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='progress'
    )

    grade = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def update_status(self):
        if self.grade is not None:
            self.status = 'done'
        else:
            self.status = 'progress'
        self.save()

