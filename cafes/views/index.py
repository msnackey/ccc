from django.http import JsonResponse
from django.views.generic.list import ListView

from cafes.models import Cafe
from reviews.models import Review


class IndexView(ListView):
    model = Cafe
    template_name = "cafes/index.html"
    context_object_name = "cafes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["top_rated_cafes"] = Cafe.objects.get_top_rated_cafes()
        context["recent_reviews"] = Review.objects.get_recent_reviews()

        return context


def cafe_data(request):
    return JsonResponse(list(Cafe.objects.values()), safe=False)
