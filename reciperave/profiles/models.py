from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe  # Import Recipe model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def recipe_count(self):
        # Count recipes where the current user is the author
        return Recipe.objects.filter(user=self.user).count()

    class Meta:
        db_table = 'tbl_profile'
