from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from profiles.models import Profile
from follows.models import Follow
from recipes.models import Recipe
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,  force_str
from django.contrib.auth import update_session_auth_hash

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def error1(request):
    return render(request, 'base/toast_notification.html')

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def custom_404(request, exception=None):
    return render(request, 'base/404.html', status=404)

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
def login_view(request):
    if request.user.is_authenticated:
        return redirect('homes')

    if request.method == "POST":
        # Extract data from POST request for login
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Manual validation for login
        if not username or not password:
            messages.error(request, 'Username and password are required.')
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin:index')
                else:
                    return redirect('homes')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login_register.html', {'form_type': 'login'})


@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('homes')

    if request.method == "POST":
        # Extract data from POST request for registration
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Manual validation for registration
        if not first_name or not last_name or not username or not email or not password1 or not password2:
            messages.error(request, 'All fields are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            # Create the user
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password1),
            )
            # Create a profile for the user
            Profile.objects.create(user=user)

            # Log in the user
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('homes')

    return render(request, 'users/login_register.html', {'form_type': 'register'})

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

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def password__reset_done(request):
    return render(request, 'forgot/password_reset_done.html')

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
            message = render_to_string('forgot/email_template.html', {
                'reset_url': reset_url,
            })
            text_content = strip_tags(message)
            email_message = EmailMultiAlternatives(
                subject='Password Reset',
                body=text_content,  # Plain text content for email clients that don't support HTML
                from_email='sbineesh172@gamil.com',
                to=[email]
            )
            email_message.attach_alternative(message, "text/html")
            email_message.send()
        return redirect('password__reset_done')  # Redirect to a confirmation page
    return render(request, 'forgot/forgot_password.html')

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def password_reset_complete(request):
    return render(request, 'forgot/password_reset_complete.html')

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def password_reset_invalid(request):
    return render(request, 'forgot/password_reset_invalid.html')

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def reset_password(request, uidb64, token):
    try:
        uid =  force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            return redirect('password_reset_complete')  # Redirect to a success page
        return render(request, 'forgot/reset_password.html')
    else:
        return redirect('password_reset_invalid')  # Redirect to an invalid token page