from django import forms

from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating"]
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} Stars") for i in range(1, 6)]),
        }
