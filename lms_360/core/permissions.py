from rest_framework.permissions import BasePermission
from courses.models import Enrollment

class IsEnrolledInCourse(BasePermission):

    """
    Allows access only to users enrolled in the course.
    """

    def has_permission(self, request, view):
        course_id = view.kwargs.get("course_id") or view.kwargs.get("pk")

        if not course_id:
            return False
        
        return Enrollment.objects.filter(
            user = request.user,
            course_id = course_id
        ).exists()


class IsEnrolledInDiscussion(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.course.enrollments.filter(
            user=request.user
        ).exists()



class IsEnrolledInAssignment(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.course.enrollments.filter(
            user=request.user
        ).exists()


class IsEnrolledInLiveLesson(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.course.enrollments.filter(
            user=request.user
        ).exists()


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'instructor'
    

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsCourseOwner(BasePermission):
    """
    Allows access only to the instructor who owns the course.
    """

    def has_object_permission(self, request, view, obj):
        return obj.instructor == request.user





