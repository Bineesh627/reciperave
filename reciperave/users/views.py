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

def custom_404(request, exception=None):
    if request.user.is_authenticated:
        template_name = 'base/404_logged_in.html'
    else:
        template_name = 'base/404_not_logged_in.html'
    return render(request, template_name, status=404)

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

    user_form = None
    form = None

    if request.method == "POST":
        if 'register' in request.POST:
            user_form = RegistrationForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
                Profile.objects.create(user=user)
                # Log in the user
                login(request, user)
                request.session['username'] = user.username  # Store username in session
                return redirect('homes')
            # If registration form is invalid, fall through to render the form with errors

        elif 'login' in request.POST:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    request.session['username'] = user.username  # Store username in session
                    if user.is_staff:  # Check if user is admin
                        return redirect('admin:index')  # Redirect to Django admin
                    else:
                        return redirect('homes')  # Redirect to user home
                else:
                    form.add_error(None, 'Invalid username or password')
            # If login form is invalid, fall through to render the form with errors

    if user_form is None:
        user_form = RegistrationForm()

    if form is None:
        form = LoginForm()

    return render(request, 'users/signin_signup.html', {'form': form, 'user_form': user_form})

def user_logout(request):
    logout(request)
    request.session.flush()  # Clear session data on logout
    return redirect('index')  

class LoginView(TemplateView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homes')  # Redirect to home if user is already logged in
        return super().get(request, *args, **kwargs)