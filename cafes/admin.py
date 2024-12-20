from django.contrib import admin

from cafes import models


@admin.register(models.Cafe)
class RatingAdmin(admin.ModelAdmin):
    model = models.Cafe
    list_display = [
        "name",
    ]
    search_fields = ["name"]
