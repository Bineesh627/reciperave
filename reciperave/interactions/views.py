from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Rating, Comments
from recipes.models import Recipe

@login_required
def rate_and_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    current_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()
    comments = Comments.objects.filter(recipe=recipe, user=request.user)

    context = {
        'recipe': recipe,
        'current_rating': current_rating.rating if current_rating else 0,
        'comments': comments
    }
    return render(request, 'interactions/rate_post.html', context)

@login_required
def submit_rating_and_comment(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(id=recipe_id)
        rating_value = request.POST.get('rating')
        comments_texts = request.POST.getlist('comments[]')

        if rating_value:
            comment_text = comments_texts[0] if comments_texts else "" 

            Rating.objects.create(
                recipe=recipe,
                user=request.user,
                rating=rating_value,
                comment=comment_text
            )
        
        for comment_text in comments_texts:
            if comment_text.strip():
                Comments.objects.create(
                    recipe=recipe,
                    user=request.user,
                    comments=comment_text
                )
        
        return redirect('homes')

@login_required
def edit_rating_and_comment(request, recipe_id, rating_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    rating = get_object_or_404(Rating, id=rating_id, recipe=recipe, user=request.user)
    comments = Comments.objects.filter(recipe=recipe, user=request.user)
    
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        comments_texts = request.POST.getlist('comments[]')

        # Update rating
        if rating_value:
            rating.rating = rating_value
            rating.comment = comments_texts[0] if comments_texts else ""  # Update comment from first entry
            rating.save()

        # Update comments
        for comment_text in comments_texts:
            if comment_text.strip():
                # Delete existing comments before adding new ones
                Comments.objects.filter(recipe=recipe, user=request.user).delete()
                Comments.objects.create(
                    recipe=recipe,
                    user=request.user,
                    comments=comment_text
                )
        
        return redirect('homes')

    context = {
        'recipe': recipe,
        'rating': rating,
        'comments': comments
    }
    return render(request, 'interactions/edit_rate_post.html', context)

