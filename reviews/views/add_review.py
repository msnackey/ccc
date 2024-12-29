from django.shortcuts import redirect, render

from cafes.models import Cafe
from reviews.forms import RatingForm, ReviewRatingFormSet


def add_review(request, id, name):
    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        formset = ReviewRatingFormSet(request.POST)

        cafe = Cafe.objects.get_or_create_from_google(id)

        if rating_form.is_valid() and formset.is_valid():
            rating = rating_form.save(commit=False)
            rating.cafe = cafe
            rating.user = request.user
            rating.save()

            reviews = formset.save(commit=False)
            for review in reviews:
                review.rating = rating
                review.cafe = cafe
                review.user = request.user
                review.save()

            return redirect("cafes:cafe_detail", id=id)
    else:
        rating_form = RatingForm()
        formset = ReviewRatingFormSet()

    return render(
        request,
        "reviews/add_review.html",
        {
            "rating_form": rating_form,
            "formset": formset,
            "cafe_name": name,
        },
    )
