from django.shortcuts import render, redirect, get_object_or_404
from . models import Bookmark
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required

@admin_required
@login_required
def bookmark_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the user has already bookmarked this recipe
    if not Bookmark.objects.filter(recipe=recipe, user=request.user).exists():
        Bookmark.objects.create(recipe=recipe, user=request.user)
    
    # Redirect to the view_bookmark page
    return redirect('view_bookmark')


@admin_required
@login_required
def view_bookmark(request):
    # Fetch all bookmarks for the current user
    bookmarks = Bookmark.objects.filter(user=request.user)
    
    # Fetch recipes associated with these bookmarks
    recipes = [bookmark.recipe for bookmark in bookmarks]
    
    context = {
        'bookmarks': bookmarks,
        'recipes': recipes,
    }
    
    return render(request, 'bookmarks/view_bookmark.html', context)

@admin_required
@login_required
def unbookmark_recipe(request, recipe_id):
    # Retrieve the recipe and check if the bookmark exists
    recipe = get_object_or_404(Recipe, id=recipe_id)
    bookmark = get_object_or_404(Bookmark, recipe=recipe, user=request.user)
    
    # Delete the bookmark
    bookmark.delete()
    
    # Redirect to the view_bookmark page or another appropriate page
    return redirect('view_bookmark')