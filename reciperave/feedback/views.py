from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Feedback
from django.contrib.auth.decorators import login_required

@login_required
def feedback(request):
    return render(request, 'feedback/feedback_form.html')

@login_required
def feedback_success(request):
    return render(request, 'feedback/feedback_success.html')

@login_required
def feedbackForm(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            user = request.user
            Feedback.objects.create(user=user, message=message)
            return redirect('feedback_success')  # Redirect to success page
        else:
            return HttpResponse("<script>alert('Feedback cannot be empty');window.location='/feedback/';</script>")
    else:
        return redirect('feedback')  # Redirect to feedback form if not POST
