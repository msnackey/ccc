from django.urls import path

from .views import add_review, submit_rating

app_name = "reviews"

urlpatterns = [
    path("rate/", submit_rating, name="submit_rating"),
    path("review/<str:id>&<str:name>/", add_review, name="add_review"),
]
