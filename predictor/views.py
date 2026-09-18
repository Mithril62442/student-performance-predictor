import joblib
from django.shortcuts import render, redirect

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