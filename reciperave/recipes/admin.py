from django.contrib import admin
from .models import Recipe, Category

class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'recipe_name', 'total_time', 'dishType', 'description', 'photo', 'video', 'instruction', 'created_at')

    def username(self, obj):
        return obj.user.username if obj.user else 'Anonymous'  # Return 'Anonymous' if user is None

    username.short_description = 'Username'  # Label for the column in the admin

    list_display = ('username', 'recipe_name', 'created_at')  # Display user and recipe details

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cid', 'dishtype')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
