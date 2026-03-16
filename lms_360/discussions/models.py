from django.db import models
from django.conf import settings
from courses.models import Course

User = settings.AUTH_USER_MODEL


class DiscussionCategory(models.Model):
    name = models.CharField(max_length = 150)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name
    

class Discussion(models.Model):
    course = models.ForeignKey(
        Course, on_delete = models.CASCADE, related_name = 'discussions'
    )
    category = models.ForeignKey(
        DiscussionCategory,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'discussions'
    )

    author = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name='discussions'
    )

    title = models.CharField(max_length=255)
    content = models.TextField()

    followers = models.ManyToManyField(
        User,
        through='DiscussionFollow',
        related_name = 'followed_discussions'
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
    
    @property
    def total_likes(self):
        return self.likes.count()
    
    @property
    def total_replies(self):
        return self.replies.count()
    
    @property
    def total_views(self):
        return self.views.count()
    


class DiscussionReply(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete = models.CASCADE, related_name = 'replies'
    )
    author = models.ForeignKey(
        User, on_delete = models.CASCADE, related_name = 'discussion_replies'
    )
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Reply by {self.author}"



class DiscussionLike(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete = models.CASCADE, related_name = 'likes'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('discussion', 'user')


class DiscussionFollow(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete = models.CASCADE
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('discussion', 'user')


class DiscussionView(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name = 'views'
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    viewed_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('discussion', 'user')



