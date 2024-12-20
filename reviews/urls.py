from django.urls import path
from .views import submit_rating

urlpatterns = [
    path("rate/", submit_rating, name="submit_rating"),
]
