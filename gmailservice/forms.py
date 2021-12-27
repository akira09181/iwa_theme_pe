from django import forms
from .models import Users

class loginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Users
        fields=('id',)