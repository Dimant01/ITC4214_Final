from django import forms
from .models import Profile
from datetime import date

class ProfileForm(forms.ModelForm):

    bio = forms.CharField(
        required=False,
        max_length=1000,
        widget=forms.Textarea(attrs={
            "rows": 5,
            "maxlength": 1000,
            "placeholder": "Write something about yourself (max 1000 characters)..."
        })
    )

    class Meta:
        model = Profile
        fields = ["bio", "location", "birth_date"]

        widgets = {
            "birth_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            )
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")

        if birth_date:
            if birth_date >= date.today():
                raise forms.ValidationError("Birth date cannot be today or in the future.")

        return birth_date

    def clean_bio(self):
        bio = self.cleaned_data.get("bio", "")

        if len(bio) > 1000:
            raise forms.ValidationError("Bio cannot exceed 1000 characters.")

        return bio