from django import forms

from company.models import Review
from show.models import ShowReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']


class ReviewShowForm(forms.ModelForm):
    class Meta:
        model = ShowReview
        fields = ['rating', 'text']
