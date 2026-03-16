from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

from courses.models import Enrollment, LessonProgress, Lesson
from users.models import User

from assignments.models import AssignmentSubmission
from dashboard.models import TodoItem
from schedule.models import LiveLesson

from .models import LearningSession


def get_recent_course_with_progress(user):
    enrollment = (
        Enrollment.objects.filter(student = user)
        .select_related('course')
        .order_by('-enrolled_at')
        .first()
    )

    if not enrollment:
        return None
    
    course = enrollment.course

    total_lessons = Lesson.objects.filter(
        section__course=course
    ).count()

    completed_lessons = LessonProgress.objects.filter(
        student=user,
        lesson__section__course=course,
        completed=True
    ).count()

    progress_percent = (
        (completed_lessons / total_lessons) * 100
        if total_lessons > 0 else 0
    )

    return{
        "course_id": course.id,
        "title": course.title,
        "completed": completed_lessons,
        "total": total_lessons,
        "progress": round(progress_percent, 1)
    }

def get_learning_hours(user):
    today = timezone.now().date()
    five_months_ago = today - timedelta(days=150)

    sessions = (
        user.learning_sessions
        .filter(start_time__date__gte=five_months_ago)
    )

    monthly_hours = {}

    for session in sessions:
        month = session.start_time.strftime('%b')
        monthly_hours.setdefault(month, 0)
        monthly_hours[month] += session.duration_hours

    return monthly_hours


def get_performance(user):
    submissions = AssignmentSubmission.objects.filter(
        student=user,
        grade__isnull=False
    )

    if not submissions.exists():
        return None
    
    avg_grade = submissions.aggregate(
        avg=Sum('grade')
    )['avg'] / submissions.count()

    return round(avg_grade, 2)


def get_todos(user):
    return list(
        TodoItem.objects
        .filter(user=user)
        .values('id', 'title', 'completed')
    )

def get_recent_enrolled_classes(user):
    enrollments = (
        Enrollment.objects
        .filter(student=user)
        .order_by('-enrolled_at')[:2]
    )

    data = []
    for e in enrollments:
        course = e.course
        data.append({
            "title": course.title,
            "duration": course.duration_hours,
            "lessons": course.sections.count(),
        })

    return data


def get_upcoming_lessons(user):
    now=timezone.now()

    lessons = (
        LiveLesson.objects
        .filter(course__enrollments__student=user, start_time__gte=now)
        .order_by('start_time')[:2]
    )

    return [
        {
            "title": l.title,
            "time": l.start_time,
            "join_url": l.join_url
        }
        for l in lessons
    ]

def start_learning_session(user, course):
    # Close any active session for this user first
    active_sessions = LearningSession.objects.filter(
        user=user,
        is_active=True
    )

    for session in active_sessions:
        session.close_session()

    # Start new session
    return LearningSession.objects.create(
        user=user,
        course=course,
        start_time=timezone.now(),
    )


def end_learning_session(user, course):
    session = LearningSession.objects.filter(
        user=user,
        course=course,
        is_active=True
    ).first()

    if session:
        session.close_session()

    return session



