import joblib

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import (
    StudentProfile,
    AcademicRecord,
    Subject,
    WeeklyGoal,
    StudySession,
    MoodEntry,
)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
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
            return redirect("create_account")

    else:
        form = ProfileForm()

    return render(
        request,
        "predictor/profile.html",
        {"form": form}
    )


def create_account(request):

    profile = request.session.get("profile")

    if not profile:
        return redirect("create_profile")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password length
        if len(password) < 8:
            messages.error(
                request,
                "Password must be at least 8 characters long."
            )
            return render(
                request,
                "predictor/signup.html"
            )

        # Uppercase letter
        if not any(char.isupper() for char in password):
            messages.error(
                request,
                "Password must contain at least one uppercase letter."
            )
            return render(
                request,
                "predictor/signup.html"
            )

        # Lowercase letter
        if not any(char.islower() for char in password):
            messages.error(
                request,
                "Password must contain at least one lowercase letter."
            )
            return render(
                request,
                "predictor/signup.html"
            )

        # Number
        if not any(char.isdigit() for char in password):
            messages.error(
                request,
                "Password must contain at least one number."
            )
            return render(
                request,
                "predictor/signup.html"
            )

        # Special character
        if not any(not char.isalnum() for char in password):
            messages.error(
                request,
                "Password must contain at least one special character."
            )
            return render(
                request,
                "predictor/signup.html"
            )

        # Password confirmation
        if password != confirm_password:
            return render(
                request,
                "predictor/signup.html"
            )

        # Username availability
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "This username is already taken."
            )
            return render(
                request,
                "predictor/signup.html"
            )

        # Create account
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # Create StudentProfile from Step 1 data
        StudentProfile.objects.create(
            user=user,
            **profile
        )

        # Remove temporary profile data
        del request.session["profile"]

        # Log the user in
        login(request, user)

        # Go to personalized dashboard
        return redirect("dashboard")

    return render(
        request,
        "predictor/signup.html"
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

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "predictor/login.html"
    )    
@login_required
def dashboard(request):

    user = request.user

    # PROFILE
    profile = getattr(
        user,
        "student_profile",
        None
    )

    # ACADEMIC PROGRESS
    academic_records = AcademicRecord.objects.filter(
        user=user
    ).order_by("created_at")

    academic_labels = [
        record.period
        for record in academic_records
    ]

    academic_values = [
        float(record.gpa)
        for record in academic_records
    ]

    # SUBJECTS
    subjects = Subject.objects.filter(
        user=user
    ).order_by("name")

    subject_data = []

    for subject in subjects:
        subject_data.append({
            "code": subject.code,
            "name": subject.name,
            "grade": subject.grade,
            "percentage": subject.percentage(),
        })

    # WEEKLY GOALS
    today = timezone.localdate()

    week_start = today - timedelta(
        days=today.weekday()
    )

    goals = WeeklyGoal.objects.filter(
        user=user,
        week_start=week_start
    )

    completed_goals = goals.filter(
        completed=True
    ).count()

    # STUDY ACTIVITY
    week_sessions = StudySession.objects.filter(
        user=user,
        date__gte=week_start,
        date__lte=today
    )

    weekly_minutes = sum(
        session.duration_minutes
        for session in week_sessions
    )

    weekly_hours = round(
        weekly_minutes / 60,
        1
    )

    # STUDY STREAK
    study_dates = set(
        StudySession.objects.filter(
            user=user
        ).values_list(
            "date",
            flat=True
        )
    )

    streak = 0

    if study_dates:

        current_date = max(study_dates)

        while current_date in study_dates:

            streak += 1

            current_date -= timedelta(days=1)

    # DAILY MOOD
    latest_mood = MoodEntry.objects.filter(
        user=user
    ).first()

    # DASHBOARD DATA
    context = {
        "profile": profile,
        "academic_labels": academic_labels,
        "academic_values": academic_values,
        "subjects": subject_data,
        "goals": goals,
        "completed_goals": completed_goals,
        "weekly_hours": weekly_hours,
        "streak": streak,
        "latest_mood": latest_mood,
    }

    return render(
        request,
        "predictor/dashboard.html",
        context
    )