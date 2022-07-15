from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views import View



class Register(View):
    def __init__(self):
        self.ctx = {}
        self.ctx['err'] = []

    def get(self, req):
        return render(req, '../templates/authenticate/register_page.html', self.ctx)

    def post(self, req):
        valid_password = True
        self.ctx['user'] = {
            'email': req.POST.get('email'),
            'first_name': req.POST.get('first_name'),
            'last_name': req.POST.get('last_name')
        }
        if req.POST.get('password1') != req.POST.get('password2'):
            self.ctx['err'].append('Passwords do not match')
            valid_password = False
        if len(req.POST.get('password1')) < 8:
            self.ctx['err'].append('Password must be at least 8 characters')
            valid_password = False
        if not valid_password:
            return render(req, '../templates/authenticate/register_page.html', self.ctx)
        new_user = CustomUser.objects.create_user(email=req.POST.get('email'), password=req.POST.get('password1'),
                                                  first_name=req.POST.get('first_name'), last_name=req.POST.get('last_name'))
        login(req, new_user)
        return redirect('/')


class Login(View):
    def __init__(self):
        self.signin = LoginUser()

    def get(self, req):
        if req.user.is_authenticated:
            return redirect('/')
        return render(req, '../templates/authenticate/login_page.html', {'signin': self.signin})

    def post(self, req):
        form = LoginUser(req.POST)
        if form.is_valid():
            email = req.POST.get('email')
            password = req.POST.get('password')
            to_login = authenticate(req, email=email, password=password)
            if to_login is not None:
                login(req, to_login)
                return redirect('/')
            else:
                return render(req, '../templates/authenticate/login_page.html', {'signin': form})

