from django.db.models import Count, Q
from .models import Discussion, DiscussionLike, DiscussionFollow, DiscussionReply, DiscussionView

def get_discussion(user, tab=None, search=None, sort=None):
    queryset = Discussion.objects.all().annotate(
        likes_count=Count('likes', distinct=True),
        replies_count=Count('replies', distinct=True),
        views_count=Count('views', distinct=True),
    )

    # Tabs logic
    if tab == 'my':
        queryset = queryset.filter(author=user)
        
    elif tab == 'following':
        queryset = queryset.filter(followers=user)

    elif tab == "unanswered":
        queryset = queryset.filter(replies__isnull=True)

    # Sorting
    if sort == 'likes':
        queryset = queryset.order_by('-replies_count')

    elif sort == 'replies':
        queryset = queryset.order_by('-replies_count')

    elif sort == 'views':
        queryset = queryset.order_by('views_count')

    else:
        queryset = queryset.order_by('-created_at')

    return queryset


def toggle_like(discussion, user):
    like, created = DiscussionLike.objects.get_or_create(
        discussion = discussion,
        user = user
    )

    if not created:
        like.delete()
        return False
    
    return True

def toggle_follow(discussion, user):
    follow, created = DiscussionFollow.objects.get_or_create(
        discussion = discussion,
        user = user
    )

    if not created:
        follow.delete()
        return False
    
    return True

def add_view(discussion, user):
    DiscussionView.objects.get_or_create(
        discussion = discussion,
        user = user
    )

def create_reply(discussion, user, content):
    return DiscussionReply.objects.create(
        discussion = discussion,
        author = user,
        content = content
    )





