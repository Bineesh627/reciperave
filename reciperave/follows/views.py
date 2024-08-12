from django.http import JsonResponse
# from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Follow
from profiles.models import Profile

@login_required
def followers(request, username):
    user = get_object_or_404(User, username=username)
    
    # Fetch users who are following the `user`
    followers = User.objects.filter(following__following=user)

    followers_list = []
    for follower in followers:
        # Get the profile associated with the follower
        profile = get_object_or_404(Profile, user=follower)
        
        followers_list.append({
            'uid': follower.id,
            'fname': follower.first_name,
            'lname': follower.last_name,
            'username': follower.username,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None,  # Adjust to your profile image field name
            'is_following_back': Follow.objects.filter(follower=user, following=follower).exists()
        })

    return render(request, 'follows/followers.html', {
        'followers_list': followers_list,
        'profile_user': user
    })

@login_required
def followings(request, username):
    user = get_object_or_404(User, username=username)
    # Fetch users whom the `user` is following using the related manager
    followings = user.following.all()

    followings_list = []
    for following in followings:
        following_user = following.following
        profile = get_object_or_404(Profile, user=following_user)
        
        followings_list.append({
            'uid': following_user.pk,
            'fname': following_user.first_name,
            'lname': following_user.last_name,
            'username': following_user.username,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
            'is_following': Follow.objects.filter(follower=request.user, following=following_user).exists()
        })

    return render(request, 'follows/following.html', {
        'followings_list': followings_list,
        'profile_user': user
    })



@login_required
def follow_user(request):
    if request.method == 'POST':
        user_id = request.POST.get("id")
        current_user = request.user

        if user_id and int(user_id) != current_user.id:
            user_to_follow = get_object_or_404(User, id=user_id)
            Follow.objects.get_or_create(follower=current_user, following=user_to_follow)
            is_followed = True
        else:
            is_followed = False

        return JsonResponse({'is_followed': is_followed})

@login_required
def unfollow_user(request):
    if request.method == 'POST':
        user_id = request.POST.get("id")
        current_user = request.user

        if user_id and int(user_id) != current_user.id:
            user_to_unfollow = get_object_or_404(User, id=user_id)
            Follow.objects.filter(follower=current_user, following=user_to_unfollow).delete()
            is_followed = False
        else:
            is_followed = True

        return JsonResponse({'is_followed': is_followed})