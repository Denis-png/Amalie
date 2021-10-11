from django import forms


class CreateUser(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'color: #2a5d68; border-color: #2a5d68;'}), required=True)
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'color: #2a5d68; border-color: #2a5d68;'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'color: #2a5d68; border-color: #2a5d68;'}), required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'color: #2a5d68; border-color: #2a5d68;'}), required=True, min_length=8)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'color: #2a5d68; border-color: #2a5d68;'}), required=True, min_length=8)


class LoginUser(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'color: #2a5d68; border-color: #2a5d68;'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'color: #2a5d68; border-color: #2a5d68;'}), required=True)

