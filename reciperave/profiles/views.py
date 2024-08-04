from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from recipes.models import Recipe
from follows.models import Follow
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        username = request.POST.get('username')
        bio = request.POST.get('bio', '')
        profile_picture = request.FILES.get('profile_picture', None)

        # Validate username uniqueness
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            # Handle the case where the username is already taken
            return render(request, 'profiles/edit_profile.html', {'error': 'Username already taken', 'user': user, 'profile': profile})

        user.username = username
        user.save()

        profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()

        return redirect('homes')

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profiles/edit_profile.html', context)

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    is_own_profile = request.user == user_profile
    recipes = Recipe.objects.all()

    # Determine if the current user is following the user_profile
    is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()

    followers = User.objects.filter(following__following=user_profile)
    followings = User.objects.filter(following__follower=user_profile)

    followers_list = [{
        'uid': follower.id,
        'fname': follower.first_name,
        'lname': follower.last_name,
        'username': follower.username,
        'is_following_back': Follow.objects.filter(follower=user_profile, following=follower).exists()
    } for follower in followers]

    followings_list = [{
        'uid': following.id,
        'fname': following.first_name,
        'lname': following.last_name,
        'username': following.username,
        'is_following': True
    } for following in followings]

    followers_count = followers.count()
    following_count = followings.count()

    profile = get_object_or_404(Profile, user=user_profile)
    recipe_count = profile.recipe_count if hasattr(profile, 'recipe_count') else 0

    context = {
        'recipes': recipes,
        'current_user': {
            'uid': user_profile.id,
            'fname': user_profile.first_name,
            'lname': user_profile.last_name,
            'username': user_profile.username,
            'bio': profile.bio,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None
        },
        'followers_list': followers_list,
        'followings_list': followings_list,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'recipe_count': recipe_count
    }
    
    return render(request, 'profiles/profile.html', context)
