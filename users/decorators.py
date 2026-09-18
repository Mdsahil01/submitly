from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def student_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a Student.
    Raises PermissionDenied (HTTP 403) if the user is logged in but not a Student.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_student:
            raise PermissionDenied("You do not have permission to access the student dashboard.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def faculty_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a Faculty member.
    Raises PermissionDenied (HTTP 403) if the user is logged in but not Faculty.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_faculty:
            raise PermissionDenied("You do not have permission to access the faculty dashboard.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
