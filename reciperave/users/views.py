from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def homes(request):
    return render(request, 'users/homes.html')

def registration(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse("<h1>Registration successfully</h1>")
    else:
        user_form = RegistrationForm()

    return render(request, 'users/register.html', {'user_form': user_form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    form.add_error(None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
                else:
                    login(request, user)
                    return redirect('homes')  # Redirect to user home
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('homes')  