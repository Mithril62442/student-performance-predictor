from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    name = models.CharField(
        max_length=100
    )

    education_level = models.CharField(
        max_length=100,
        blank=True
    )

    current_year = models.CharField(
        max_length=50,
        blank=True
    )

    institution = models.CharField(
        max_length=150,
        blank=True
    )

    term = models.CharField(
        max_length=50,
        blank=True
    )

    academic_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class AcademicRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="academic_records"
    )

    period = models.CharField(
        max_length=50
    )

    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.period}"


class Subject(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    code = models.CharField(
        max_length=30,
        blank=True
    )

    name = models.CharField(
        max_length=150
    )

    marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    maximum_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=100
    )

    grade = models.CharField(
        max_length=10,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def percentage(self):
        if self.marks is None or not self.maximum_marks:
            return 0

        return round(
            float(self.marks) /
            float(self.maximum_marks) *
            100,
            1
        )

    def __str__(self):
        return self.name


class WeeklyGoal(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="weekly_goals"
    )

    title = models.CharField(
        max_length=200
    )

    week_start = models.DateField()

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.title


class StudySession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_sessions"
    )

    date = models.DateField(
        default=timezone.now
    )

    duration_minutes = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class MoodEntry(models.Model):

    MOOD_CHOICES = [
        ("great", "Great"),
        ("good", "Good"),
        ("okay", "Okay"),
        ("low", "Low"),
        ("stressed", "Stressed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mood_entries"
    )

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES
    )

    date = models.DateField(
        default=timezone.now
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.mood}"