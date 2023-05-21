from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(required=True, widget=forms.PasswordInput)
