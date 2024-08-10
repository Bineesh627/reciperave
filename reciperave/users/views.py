from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from profiles.models import Profile
from follows.models import Follow
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control

@login_required
def homes(request):
    # Get the logged-in user
    current_user = request.user

    # Get all profiles except the logged-in user's profile
    profiles = Profile.objects.exclude(user=current_user)

    # Prepare data for the template
    profile_data = []

    for profile in profiles:
        # Check if the logged-in user is following the profile user
        is_followed = Follow.objects.filter(follower=current_user, following=profile.user).exists()
        profile_data.append({
            'profile': profile,
            'is_followed': is_followed,
        })

    return render(request, 'users/homes.html', {'profile_data': profile_data})


@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def registration(request):
    if request.user.is_authenticated:
        return redirect('homes') 

    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            Profile.objects.create(user=user)
            # Log in the user
            login(request, user)
            return redirect('homes')
    else:
        user_form = RegistrationForm()

    return render(request, 'users/register.html', {'user_form': user_form})

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('homes') 

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homes')  # Redirect to user home
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    if request.user.is_authenticated:
        return redirect('homes') 

    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  

from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homes')  # Redirect to home if user is already logged in
        return super().get(request, *args, **kwargs)