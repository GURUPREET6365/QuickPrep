from django import forms
from .models import UsersGoals

class EditGoalForm(forms.ModelForm):
    class Meta:
        model = UsersGoals
        fields = ["title", "description"]
