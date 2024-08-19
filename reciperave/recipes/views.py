from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RecipeForm
from .models import Recipe, Category
from bookmarks.models import Bookmark
from profiles.models import Profile
from django.contrib import messages
from interactions.models import Rating, Comments
from django.contrib.auth.decorators import login_required

@login_required
def upload_recipe(request):
    categories = Category.objects.all()  # Fetch categories using ORM
    return render(request, 'recipes/upload_recipe.html', {'categories': categories})

@login_required
def upload_recipe_action(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Ensure the user is set correctly
            recipe.save()

            # Success message
            messages.success(request, 'Your recipe has been uploaded successfully!')
            return redirect('upload_recipe')
        else:
            # Error message
            messages.error(request, 'There was an error in your recipe submission. Please check the form and try again.')
    else:
        form = RecipeForm()

        # Info message to guide the user
        messages.info(request, 'Please fill out the form to upload a new recipe.')

    return render(request, 'recipes/upload_recipe.html', {'form': form})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Use ORM to get recipe or return 404
    categories = Category.objects.all()  # Fetch categories using ORM
    context = {
        'recipe': recipe,
        'categories': categories,
        'recipe_id': recipe_id
    }
    return render(request, 'recipes/edit_recipe.html', context)

@login_required
def edit_recipe_action(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Use ORM to get recipe or return 404
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('homes')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form})

@login_required
def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    is_author = request.user == recipe.user
    user = recipe.user
    profile = get_object_or_404(Profile, user=user)
    is_bookmarked = Bookmark.objects.filter(recipe=recipe, user=request.user).exists()
    ratings = Rating.objects.filter(recipe=recipe)
    comments = Comments.objects.filter(recipe=recipe)
    current_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()
    user_comments = Comments.objects.filter(recipe=recipe, user=request.user)

    context = {
        'recipe': recipe,
        'ratings': ratings,
        'comments': comments,
        'current_rating': current_rating,
        'user_comments': user_comments,
        'is_bookmarked': is_bookmarked,
        'is_author': is_author,
        'profile': profile,
    }

    return render(request, 'recipes/view_recipe.html', context)

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Use ORM to get recipe or return 404
    try:
        recipe.delete()  # Delete the recipe using ORM
        return redirect('homes')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")