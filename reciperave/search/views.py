from django.shortcuts import render
from recipes.models import Recipe, Category
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required

@admin_required
@login_required
def search_recipes(request):
    title = request.GET.get('title', '')
    dish_type = request.GET.get('dishType', '')

    recipes = Recipe.objects.all()

    if title:
        recipes = recipes.filter(recipe_name__icontains=title)

    if dish_type:
        recipes = recipes.filter(dishType=dish_type)

    # Get all categories for the filter dropdown
    categories = Category.objects.all()

    context = {
        'recipes': recipes,
        'categories': categories,
        'selected_dish_type': dish_type
    }

    return render(request, 'search/search_recipes.html', context)
