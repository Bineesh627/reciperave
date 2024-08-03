from django.contrib import admin
from .models import Rating, Comments

class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'rating', 'comment', 'created_at')
    list_filter = ('recipe', 'user', 'rating')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'comments', 'created_at')
    list_filter = ('recipe', 'user')

admin.site.register(Rating, RatingAdmin)
admin.site.register(Comments, CommentsAdmin)
