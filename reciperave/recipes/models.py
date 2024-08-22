from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    dishtype = models.CharField(max_length=50)

    class Meta:
        db_table = "tbl_categories"  # Ensure this matches your actual table name

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=70)
    total_time = models.CharField(max_length=20)
    dishType = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(upload_to='recipes/images/', null=True, blank=True)
    video = models.FileField(upload_to='recipes/videos/', null=True, blank=True)
    instruction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_recipe"  # Ensure this matches your actual table name