from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html

class ReadOnlyUserAdmin(DefaultUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Restrict normal users to view only their own details
        return qs.filter(id=request.user.id)

    list_display = ('display_username', 'first_name', 'last_name', 'email', 'user_type', 'date_joined')
    readonly_fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'user_type')

    def display_username(self, obj):
        # Render username as plain text, not a link
        return format_html('<span>{}</span>', obj.username)

    display_username.short_description = 'Username'  # Label for the column in the admin

    def user_type(self, obj):
        return 'Admin' if obj.is_superuser else 'Regular User'

    user_type.short_description = 'User Type'  # Label for the column in the admin

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Unregister the default User admin and register the custom admin
admin.site.unregister(User)
admin.site.register(User, ReadOnlyUserAdmin)
