from django.urls import path

from cafes.views import CafeDetailView, CafeListView

app_name = "cafes"

urlpatterns = [
    path("", CafeListView.as_view(), name="cafe_list"),
    path("cafe/<str:id>/", CafeDetailView.as_view(), name="cafe_detail"),
]
