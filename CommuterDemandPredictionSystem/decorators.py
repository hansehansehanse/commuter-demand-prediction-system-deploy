# from django.shortcuts import redirect
# from functools import wraps

# def access_level_required(*allowed_levels):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 return redirect('/cdps/login/')
#             if hasattr(request.user, 'access_level') and request.user.access_level in allowed_levels:
#                 return view_func(request, *args, **kwargs)
#             return redirect('/cdps/login/')  # or a "403 Forbidden" page
#         return _wrapped_view
#     return decorator

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def access_level_required(*allowed_levels):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/cdps/login/')
            if hasattr(request.user, 'access_level') and request.user.access_level in allowed_levels:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied  # returns a 403 Forbidden page
        return _wrapped_view
    return decorator
