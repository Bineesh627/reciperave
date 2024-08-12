from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from profiles.models import Profile
from follows.models import Follow
from recipes.models import Recipe
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

@login_required
def homes(request):
    # Get the logged-in user
    current_user = request.user

    # Get all profiles except the logged-in user's profile
    profiles = Profile.objects.exclude(user=current_user)

    # Get all recipes, ordered by creation date (newest first)
    recipes = Recipe.objects.all().order_by('-created_at')[:9]

    # Prepare data for the template
    profile_data = []
    for profile in profiles:
        # Check if the logged-in user is following the profile user
        is_followed = Follow.objects.filter(follower=current_user, following=profile.user).exists()
        profile_data.append({
            'profile': profile,
            'is_followed': is_followed,
        })

    context = {
        'profile_data': profile_data,
        'recipes': recipes
    }

    return render(request, 'users/homes.html', context)


@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def index(request):
    if request.user.is_authenticated:
        return redirect('homes') 
    return render(request, 'users/index.html')

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def signin_signup(request):
    if request.user.is_authenticated:
        return redirect('homes')

    form = LoginForm()  # Initialize LoginForm
    user_form = RegistrationForm()  # Initialize RegistrationForm

    if request.method == "POST":
        if 'register' in request.POST:
            user_form = RegistrationForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
                Profile.objects.create(user=user)
                login(request, user)
                return redirect('homes')
        elif 'login' in request.POST:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('homes')
                else:
                    form.add_error(None, 'Invalid username or password')

    return render(request, 'users/signin_signup.html', {'form': form, 'user_form': user_form})

def user_logout(request):
    logout(request)
    return redirect('index')  

class LoginView(TemplateView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homes')  # Redirect to home if user is already logged in
        return super().get(request, *args, **kwargs)