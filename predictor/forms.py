from django import forms


class ProfileForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Your Name",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your name"
        })
    )

    education_level = forms.ChoiceField(
        choices=[
            ("school", "School"),
            ("college", "College"),
            ("university", "University"),
        ],
        label="Education Level"
    )

    current_year = forms.CharField(
        max_length=50,
        label="Current Class / Year",
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. Class 12 / 2nd Year"
        })
    )

    institution = forms.CharField(
        max_length=150,
        label="School / College / University",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your institution"
        })
    )

    academic_year = forms.CharField(
        max_length=20,
        label="Academic Year",
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. 2026-27"
        })
    )

    term = forms.CharField(
        max_length=50,
        label="Semester / Term",
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. Semester 1"
        })
    )

    maximum_marks = forms.IntegerField(
        min_value=1,
        label="Maximum Marks",
        widget=forms.NumberInput(attrs={
            "placeholder": "e.g. 100"
        })
    )