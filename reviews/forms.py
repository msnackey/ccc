from django import forms
from django.forms import inlineformset_factory

from .models import Rating, Review


class RatingForm(forms.ModelForm):
    """Form for Rating model."""

    class Meta:
        model = Rating
        fields = ["rating"]
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} Stars") for i in range(1, 6)]),
        }


class ReviewForm(forms.ModelForm):
    """Form for Review model."""

    class Meta:
        model = Review
        fields = ["title", "content"]


ReviewRatingFormSet = inlineformset_factory(
    parent_model=Rating,
    model=Review,
    fields=("title", "content"),
    extra=1,
    can_delete=False,
)
