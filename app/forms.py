from django import forms
from .models import Import

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Import
        fields = ['file']