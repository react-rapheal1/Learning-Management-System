from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Course(models.Model):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    price = models.DecimalField(max_digits=6, decimal_places=2)
    language = models.CharField(max_length=50)
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES
    )

    duration_hours = models.DecimalField(max_digits=5, decimal_places=2)
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    intro_video_url = models.URLField(blank=True, null=True)

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='sections'
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    

class Lesson(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='lessons'
    )
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration_minutes = models.PositiveIntegerField()
    is_preview = models.BooleanField(default=False)
    order = models.PositiveIntegerField()

    def total_lessons_in_course(self):
        return Lesson.objects.filter(section__course=self.section.course).count()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
        

class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"


class LessonProgress(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name = 'lesson_progress'
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')



