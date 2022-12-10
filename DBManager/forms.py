from django import forms

from .models import *


class TableForm(forms.Form):
    name = forms.CharField(required=True)
    # data = forms.HiddenInput()
    database = forms.HiddenInput()


