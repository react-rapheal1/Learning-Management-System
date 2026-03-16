from django.urls import path
from .views import dashboard_summary, StartLearningSessionView, EndLearningSessionView, TodoListView, TodoDetailView

urlpatterns = [
    path('summary/', dashboard_summary),
    path('start-session/<int:course_id>/', StartLearningSessionView.as_view()),
    path('end-session/<int:course_id>/', EndLearningSessionView.as_view()),
    path('todos/', TodoListView.as_view()),
    path('todos/<int:pk>/', TodoDetailView.as_view()),
]