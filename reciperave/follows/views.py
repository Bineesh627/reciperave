from django.http import JsonResponse
# from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Follow

@login_required
def followers(request, username):
    user = get_object_or_404(User, username=username)
    # Fetch users who are following the `user`
    followers = User.objects.filter(following__following=user)

    followers_list = [{
        'uid': follower.id,
        'fname': follower.first_name,
        'lname': follower.last_name,
        'username': follower.username,
        'is_following_back': Follow.objects.filter(follower=user, following=follower).exists()
    } for follower in followers]

    return render(request, 'follows/followers.html', {
        'followers_list': followers_list,
        'profile_user': user
    })

@login_required
def followings(request, username):
    user = get_object_or_404(User, username=username)
    # Fetch users whom the `user` is following using the related manager
    followings = user.following.all()

    followings_list = [{
        'uid': following.following.pk,  # Access the 'following' user
        'fname': following.following.first_name,  # Access from the 'following' user
        'lname': following.following.last_name,  # Access from the 'following' user
        'username': following.following.username,  # Access from the 'following' user

        'is_following': Follow.objects.filter(follower=request.user, following=following.following).exists()
    } for following in followings]

    return render(request, 'follows/following.html', {
        'followings_list': followings_list,
        'profile_user': user
    })

@login_required
def following(request, username):
    user = get_object_or_404(User, username=username)
    # Fetch users whom the `user` is following using the related manager
    followings = user.following.all()

    followings_list = [{
        'uid': following.following.pk,  # Corrected to access the 'following' user
        'fname': following.following.first_name,  # Access from the 'following' user
        'lname': following.following.last_name,  # Access from the 'following' user
        'username': following.following.username,  # Access from the 'following' user
        'profile_picture': following.following.profile_picture.url if following.following.profile_picture else "{% static 'profiles/images/no-profile.png' %}",  # Include profile image URL
        'is_following': Follow.objects.filter(follower=request.user, following=following.following).exists()
    } for following in followings]

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