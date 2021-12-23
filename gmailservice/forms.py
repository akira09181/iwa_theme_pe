from django import forms
from .models import Users

class loginForm(forms.ModelForm):
    class Meta:
        model=Users
        fields=('id','pas')