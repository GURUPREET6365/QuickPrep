from django import forms
from .models import Streak

# This form is for editing the form.
class StreakForm(forms.ModelForm):
    # meta is used for customization of the specific database and specific things in the database.
    class Meta:
        model = Streak #tells Django “build a form based on the Streak model.”
        fields = ['title', 'description'] #“include only these two fields in the form.” You could include any editable model field here—e.g., 'is_active' if you want a checkbox to deactivate a streak.