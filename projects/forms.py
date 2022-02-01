from django import forms
from .models import Project

class NewProject(forms.ModelForm):

    name = forms.CharField(max_length = 200, help_text="Name Your Project")

    class Meta:
        model = Project
        fields = ['name']
