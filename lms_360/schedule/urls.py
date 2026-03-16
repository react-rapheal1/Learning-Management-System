from django.urls import path
from .views import LiveLessonListView, InstructorLiveLessonListView

urlpatterns = [
    path('list/', LiveLessonListView.as_view()),
    path('instructor/list/', InstructorLiveLessonListView.as_view()),
]