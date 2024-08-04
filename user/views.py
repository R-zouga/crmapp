from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views
from django.shortcuts import render, redirect, reverse
from user import models


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse(f"{user.current_status.lower()}-dashboard"))
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


