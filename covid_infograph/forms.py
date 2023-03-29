from django import forms
from datetime import date


class SearchForm(forms.Form):
    search = forms.CharField(
        label='Search', max_length=100, min_length=3, required=True)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
