from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin:index')
            return view_func(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
