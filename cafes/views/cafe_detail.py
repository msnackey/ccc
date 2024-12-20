from django.http import Http404
from django.views.generic import DetailView

from cafes.models import Cafe


class CafeDetailView(DetailView):
    model = Cafe
    template_name = "cafes/cafe_detail.html"
    context_object_name = "cafe"

    def get_object(self):
        try:
            return Cafe.objects.get(google_place_id=self.kwargs["id"])
        except Cafe.DoesNotExist:
            raise Http404("Cafe not found")

    # Optional: Override get_context_data to add extra context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context if necessary
        return context
