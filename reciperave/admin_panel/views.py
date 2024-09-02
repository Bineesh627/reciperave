from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse

class CustomAdminLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect authenticated users away from the admin login page
            return redirect('homes')  # or any other page you want to redirect to
        return super().get(request, *args, **kwargs)
