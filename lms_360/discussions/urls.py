from django.urls import path
from .views import (
    DiscussionListView,
    DiscussionLikeView,
    DiscussionFollowView,
    DiscussionReplyView,
    DiscussionDetailView,
)

urlpatterns = [
    path('', DiscussionListView.as_view()),
    path('<int:pk>/', DiscussionDetailView.as_view()),
    path('<int:pk>/like/', DiscussionLikeView.as_view()),
    path('<int:pk>/follow/', DiscussionFollowView.as_view()),
    path('<int:pk>/reply/', DiscussionReplyView.as_view()),
]
