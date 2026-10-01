from django import forms


class ProfileForm(forms.Form):

    name = forms.CharField(
        max_length=100
    )

    education_level = forms.CharField(
        max_length=100
    )

    current_year = forms.CharField(
        max_length=50
    )

    institution = forms.CharField(
        max_length=150
    )

    term = forms.CharField(
        max_length=50
    )

    academic_year = forms.CharField(
        max_length=20
    )