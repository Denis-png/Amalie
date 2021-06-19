from django import forms


class CreateUser(forms.Form):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=8)


class LoginUser(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

