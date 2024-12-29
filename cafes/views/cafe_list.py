from django.db.models import Q
from django.views.generic.list import ListView

from cafes.forms import CafeFilterForm
from cafes.models import Cafe


class CafeListView(ListView):
    """List view of all rated or reviewed cafes."""

    model = Cafe
    template_name = "cafes/cafe_list.html"
    context_object_name = "cafes"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CafeFilterForm()
        return context
