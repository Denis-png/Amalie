from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views import View



class Register(View):
    def __init__(self):
        self.signup = CreateUser()

    def get(self, req):
        return render(req, '../templates/authenticate/register_page.html', {'signup': self.signup})

    def post(self, req):
        if req.method == 'POST':
            form = CreateUser(req.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if cd['password1'] != cd['password2']:
                    err = 'Sorry, passwords do not match'
                    return render(req, '../templates/authenticate/register_page.html', {'signup': form, 'err': err})
                else:
                    new_user = CustomUser.objects.create_user(email=cd['email'], password=cd['password1'], first_name=cd['first_name'], last_name=cd['last_name'])
                    login(req, new_user)
                    return redirect('/query/select')
            else:
                return render(req, '../templates/authenticate/register_page.html', {'signup': form})


class Login(View):
    def __init__(self):
        self.signin = LoginUser()

    def get(self, req):
        if req.user.is_authenticated:
            return redirect('/home/')
        return render(req, '../templates/authenticate/login_page.html', {'signin': self.signin})

    def post(self, req):
        form = LoginUser(req.POST)
        if form.is_valid():
            email = req.POST.get('email')
            password = req.POST.get('password')
            to_login = authenticate(req, email=email, password=password)
            if to_login is not None:
                login(req, to_login)
                return redirect('/home/')
            else:
                return render(req, '../templates/authenticate/login_page.html', {'signin': form})

