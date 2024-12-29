from django import forms


class CafeFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter cafe name..."}
        ),
    )
