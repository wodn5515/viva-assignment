from django.contrib import admin
from apps.accounts.models.users import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "created_at",
    )

    list_display_links = (
        "name",
        "email",
    )
