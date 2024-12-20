from django.contrib import admin

from cafes import models


@admin.register(models.Cafe)
class RatingAdmin(admin.ModelAdmin):
    model = models.Cafe
    list_display = ["name", "google_place_id"]
    search_fields = ["name", "google_place_id"]
