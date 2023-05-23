from django import forms 
from .models import ReviewRating



class   ReviewForm(forms.MoselForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']