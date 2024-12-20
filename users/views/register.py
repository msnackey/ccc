from django.views.generic import View
from django.shortcuts import render, redirect

from users.forms import RegisterForm


class RegisterView(View):
    """User registration view"""

    template_name = "users/register.html"
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("users:login")
        context = {"form": forms}
        return render(request, self.template_name, context)
