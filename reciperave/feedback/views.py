from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required

@admin_required
@login_required
def feedback(request):
    return render(request, 'feedback/feedback_form.html')

@admin_required
@login_required
def feedback_success(request):
    return render(request, 'feedback/feedback_success.html')

@admin_required
@login_required
def feedbackForm(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            user = request.user
            Feedback.objects.create(user=user, message=message)
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback_success')  # Redirect to success page
        else:
            messages.error(request, 'Feedback cannot be empty.')
            return redirect('feedback')  # Redirect back to feedback form
    else:
        return redirect('feedback')  # Redirect to feedback form if not POST
