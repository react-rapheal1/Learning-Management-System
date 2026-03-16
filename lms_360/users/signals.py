from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.dispatch import receiver


User = get_user_model()


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    student_group, _ = Group.objects.get_or_create(name = 'Student')
    instructor_group, _ = Group.objects.get_or_create(name = 'Instructor')


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        try:
            group = Group.objects.get(name=instance.role.capitalizer())
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass



