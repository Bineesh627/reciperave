# context_processors.py
def current_url(request):
    return {
        'current_url': request.path,
        'username': request.user.username if request.user.is_authenticated else ''
    }
