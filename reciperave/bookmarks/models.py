from django.db import models
from recipes.models import Recipe
from django.contrib.auth.models import User

class Bookmark(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_bookmark'