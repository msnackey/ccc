from django.contrib import admin

from reviews import models


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    model = models.Rating
    list_display = [
        "name",
        "user",
        "cafe",
        "rating",
        "date",
    ]
    search_fields = ["user", "cafe"]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    model = models.Review
    list_display = [
        "title",
        "user",
        "cafe",
        "rating",
        "date",
    ]
    search_fields = ["title", "content", "user", "cafe"]
