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
    """
    Displays a list of users the specified user is following.
    """
    user = get_object_or_404(User, username=username)
    # Fetch users whom the `user` is following using the related manager
    followings = user.following.all()

    followings_list = [{
        'uid': following.following.pk,  # Corrected to access the 'following' user
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
def follow_user(request):
    uid1 = request.GET.get('id')  # Changed to POST
    if uid1:
        user_to_follow = get_object_or_404(User, id=uid1)
        if user_to_follow != request.user:
            # Create a follow relationship if it doesn't exist
            if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
                Follow.objects.create(follower=request.user, following=user_to_follow)
    
    # Use the correct username here
    return redirect('profile', username=user_to_follow.username)  # Redirect back to the profile page

@login_required
def unfollow_user(request):
    uid1 = request.GET.get('id')
    if uid1:
        user_to_unfollow = get_object_or_404(User, id=uid1)
        if user_to_unfollow != request.user:
            # Delete the follow relationship if it exists
            Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    
    # Use the correct username here
    return redirect('profile', username=user_to_unfollow.username)
