from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', max_length=100)

