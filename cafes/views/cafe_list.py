from django.utils import timezone
from django.views.generic.list import ListView

from cafes.models import Cafe


class CafeListView(ListView):
    model = Cafe
    template_name = "cafes/cafe_list.html"
    context_object_name = "cafes"

    # Optional: Override get_context_data to add extra context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context if necessary
        return context
