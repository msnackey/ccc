from django.urls import path

from .views import add_rating, add_review

app_name = "reviews"

urlpatterns = [
    path("rate/", add_rating, name="submit_rating"),
    path("review/<str:id>&<str:name>/", add_review, name="add_review"),
]
