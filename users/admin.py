from django.contrib import admin

from users import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    model = models.User
    list_display = [
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_superuser", "is_staff", "is_active"]
    search_fields = ["username", "email"]
