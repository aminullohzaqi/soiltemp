from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inputForm import models

def index(request):
    context = {
        'judul': 'Login'
    }
    user = None
    if request.method == "POST":
        username_login = request.POST['username']
        password_login = request.POST['password']
        
        user = authenticate(request, username=username_login, password=password_login)
        
        if user is not None :
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('index')
        
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'login.html', context)    

@login_required
def logoutView(request):
    context = {
        'judul': 'Logout'
    }
    if request.method == "POST":
        if request.POST["logout"] == "Submit":
            logout(request)
            return redirect('index')
        
    return render(request, 'logout.html', context)