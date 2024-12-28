from django.urls import path

from cafes.views import CafeDetailView, CafeListView, IndexView, cafe_data

app_name = "cafes"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("cafelist", CafeListView.as_view(), name="cafe_list"),
    path("cafe/<str:id>/", CafeDetailView.as_view(), name="cafe_detail"),
    path("api/cafes/", cafe_data, name="cafe_data"),
]
