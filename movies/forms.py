from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Review form"""
    class Meta:
        model = Review
        fields = ("name", "text")
