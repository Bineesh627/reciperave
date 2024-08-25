from django.contrib import admin
from .models import Rating

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'rating', 'created_at')

    def username(self, obj):
        return obj.user.username if obj.user else 'Anonymous'
    
    def recipe_title(self, obj):
        return obj.recipe.recipe_name if obj.recipe else 'No Recipe'

    username.short_description = 'Username'
    recipe_title.short_description = 'Recipe Title'

    list_display = ('username', 'recipe_title', 'rating', 'created_at')  # Display user and feedback details

    # Optionally, hide the 'Add' and 'Delete' buttons
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Rating, RatingAdmin)