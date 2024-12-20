from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import View

from users.forms import LoginForm


class LoginView(View):
    """User registration view"""

    template_name = "users/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data["username"]
            password = forms.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("ccc:index")
        context = {"form": forms}
        return render(request, self.template_name, context)
