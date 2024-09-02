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

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,  force_str
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django import forms
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.views.generic import TemplateView
from users.decorators import admin_required

def error1(request):
    return render(request, 'base/toast_notification.html')

@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def custom_404(request, exception=None):
    return render(request, 'base/404.html', status=404)

class LoginView(TemplateView):
    template_name = 'users/login_register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homes')  # Redirect to home if user is already logged in
        return super().get(request, *args, **kwargs)

@admin_required
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

@admin_required
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def index(request):
    if request.user.is_authenticated:
        return redirect('homes') 
    return render(request, 'users/index.html')

@admin_required
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('homes')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        # Manual validation for login
        if not username or not password:
            messages.error(request, 'Username and password are required.')
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Handle "Remember Me" functionality
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks in seconds     
                else:
                    request.session.set_expiry(0)  # Session expires on browser close

                # Redirect based on user type
                if user.is_staff:
                    return redirect('admin:index')
                else:
                    return redirect('homes')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login_register.html', {'form_type': 'login'})

@admin_required
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
        remember_me = request.POST.get('remember_me')  

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

            if remember_me:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            
            messages.success(request, 'Registration successful.')
            return redirect('homes')

    return render(request, 'users/login_register.html', {'form_type': 'register'})

def user_logout(request):
    logout(request)
    request.session.flush()  # Clear session data on logout
    return redirect('index')  

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)

@admin_required
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('homes')

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                user_name = user.username
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
                message = render_to_string('forgot/email_template.html', {
                    'reset_url': reset_url,
                    'user_name': user_name,
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
                messages.success(request, 'Password reset link has been sent to your email.')
            else:
                messages.error(request, 'No account found with this email.')
            return redirect('forgot_password')
        else:
            messages.error(request, 'Please enter a valid email address.')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot/forgot_password.html', {'form': form})

@admin_required
@cache_control(no_store=True, must_revalidate=True, no_cache=True)
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirmPassword']

            # Validate the passwords
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'forgot/reset_password.html', {'uidb64': uidb64, 'token': token})

            if len(new_password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return render(request, 'forgot/reset_password.html', {'uidb64': uidb64, 'token': token})

            if not any(char.isdigit() for char in new_password):
                messages.error(request, 'Password must include at least one number.')
                return render(request, 'forgot/reset_password.html', {'uidb64': uidb64, 'token': token})

            if not any(char.isalpha() for char in new_password):
                messages.error(request, 'Password must include at least one letter.')
                return render(request, 'forgot/reset_password.html', {'uidb64': uidb64, 'token': token})

            if not any(char in "!$@％" for char in new_password):
                messages.error(request, 'Password must include at least one special character (!$@％).')
                return render(request, 'forgot/reset_password.html', {'uidb64': uidb64, 'token': token})

            # If validation passes, set the new password
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password has been successfully reset.')
            return redirect('login')  # Redirect to the login page if successful
        return render(request, 'forgot/reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('login')