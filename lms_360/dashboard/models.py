from datetime import timezone
from django.db import models
from django.conf import settings
from courses.models import Course

User = settings.AUTH_USER_MODEL

class TodoItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='todos'
    )
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class LearningSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learning_sessions'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='learning_sessions'
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    duration_hours = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def close_session(self):
        if self.is_active:
            self.end_time = timezone.now()
            duration = self.end_time - self.start_time
            self.duration_hours = duration.total_seconds() / 3600
            self.is_active = False
            self.save()

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
