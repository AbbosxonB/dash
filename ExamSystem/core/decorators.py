from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import login_required


def role_required(allowed_roles):
    """
    Decorator that checks if the user has one of the allowed roles.
    Usage: @role_required(['Admin', 'Teacher'])
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Return forbidden response or redirect based on your needs
                return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator


def redirect_based_on_role(view_func):
    """
    Decorator that redirects user based on their role after login.
    """
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = request.user.role
        
        if user_role == 'Admin':
            return redirect('admin_dashboard')  # or just 'admin:index'
        elif user_role == 'Teacher':
            return redirect('teacher_dashboard')
        elif user_role == 'Student':
            return redirect('student_dashboard')
        else:
            # Default redirect if role is not recognized
            return redirect('login')
    
    return _wrapped_view