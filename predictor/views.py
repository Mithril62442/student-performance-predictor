import joblib

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import ProfileForm


model = joblib.load("student_performance_model.pkl")


def home(request):
    return render(request, "predictor/home.html")


def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            request.session["profile"] = form.cleaned_data
            return redirect("home")

    else:
        form = ProfileForm()

    return render(
        request,
        "predictor/profile.html",
        {"form": form}
    )


def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "predictor/login.html")