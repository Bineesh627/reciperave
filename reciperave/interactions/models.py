from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

class Comments(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.recipe.title}'

    class Meta:
        db_table = 'tbl_comments'

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rating {self.rating} by {self.user.username} for {self.recipe.title}'

    class Meta:
        db_table = 'tbl_rating'
        unique_together = ('recipe', 'user')  # Ensure each user can rate a recipe only once