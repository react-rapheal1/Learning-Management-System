from django.db import models
from django.conf import settings
from courses.models import Course

User = settings.AUTH_USER_MODEL


class LiveLesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name = 'live_lessons'
    )
    title = models.CharField(max_length=255)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='live_lessons'
    )
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    meeting_link = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


