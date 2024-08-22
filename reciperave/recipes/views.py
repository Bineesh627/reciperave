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
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    categories = Category.objects.all()

    # Split the instructions before passing to the template
    instructions_list = recipe.instruction.split('|') if recipe.instruction else []

    if request.method == "POST":
        recipe_name = request.POST.get('recipe_name')
        total_time = request.POST.get('total_time')
        dish_type = request.POST.get('dishType')
        description = request.POST.get('description')
        instructions = request.POST.getlist('instructions[]')  # Fetch the list of instructions
        photo = request.FILES.get('photo')
        video = request.FILES.get('video')

        # Only update fields if new data is provided, otherwise keep existing data
        if recipe_name:
            recipe.recipe_name = recipe_name
        if total_time:
            recipe.total_time = total_time
        if dish_type:
            recipe.dishType = dish_type
        if description:
            recipe.description = description
        
        # Update instructions only if provided; otherwise, retain existing instructions
        if instructions:
            recipe.instruction = "\n".join(instructions)
        
        if photo:
            recipe.photo = photo
        if video:
            recipe.video = video
        
        recipe.save()

        messages.success(request, 'Your recipe has been updated successfully!')
        return redirect('homes')
    else:
        messages.error(request, 'There was an error in your recipe update. Please check the form and try again.')

    context = {
        'recipe': recipe,
        'categories': categories,
        'recipe_id': recipe_id,
        'instructions_list': instructions_list,
    }
    return render(request, 'recipes/edit_recipe.html', context)

@login_required
def upload_recipe(request):
    categories = Category.objects.all()  
    if request.method == "POST":
        recipe_name = request.POST.get('recipe_name')
        total_time = request.POST.get('total_time')
        dish_type = request.POST.get('dishType')
        description = request.POST.get('description')
        instructions = request.POST.getlist('instructions[]')
        photo = request.FILES.get('photo')
        video = request.FILES.get('video')

        if recipe_name and total_time and dish_type and description and instructions:
            # Create a new Recipe object
            recipe = Recipe.objects.create(
                recipe_name=recipe_name,
                total_time=total_time,
                dishType=dish_type,
                description=description,
                instruction="\n".join(instructions),  # Join instructions into a single string
                photo=photo,
                video=video,
                user=request.user
            )
            recipe.save()

            messages.success(request, 'Your recipe has been uploaded successfully!')
            return redirect('upload_recipe')
        else:
            messages.error(request, 'There was an error in your recipe submission. Please check the form and try again.')
    context = {
        'categories': categories,
    }

    return render(request, 'recipes/upload_recipe.html', context)

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