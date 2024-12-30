from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from reviews.forms import RatingForm


@login_required
def add_rating(request):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Thank you for your rating!")  # Simple response
    else:
        form = RatingForm()
    return render(request, "reviews/rating.html", {"form": form})
