# myapp/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class AdminLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the admin login page
        if request.path == reverse('admin:login') and request.user.is_authenticated:
            # Redirect authenticated users from the admin login page
            return redirect('homes')  # or any other page you want to redirect to
        
        response = self.get_response(request)
        return response
