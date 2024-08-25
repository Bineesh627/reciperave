from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'message', 'created_at')  # Make fields read-only
    
    def username(self, obj):
        return obj.user.username if obj.user else 'Anonymous'  # Return 'Anonymous' if user is None

    username.short_description = 'Username'  # Label for the column in the admin

    list_display = ('username', 'message', 'created_at')  # Display user and feedback details

    # Optionally, hide the 'Add' and 'Delete' buttons
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Feedback, FeedbackAdmin)
