from django import forms
from .models import ultimateGoal

class UltimateGoalForm(forms.ModelForm):
    class Meta:
        model = ultimateGoal
        fields = ['title']