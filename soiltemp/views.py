from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inputForm import models

def index(request):
    user    = None
    error   = ""

    if request.method == "POST":
        username_login = request.POST['username']
        password_login = request.POST['password']
        
        user = authenticate(request, username=username_login, password=password_login)
        
        if user is not None :
            login(request, user)
            return redirect('dashboard')
        else:
            error = "User atau Password tidak Valid"
            #return redirect('index')
    context = {
        'judul': 'Login',
        'error': error,
    }

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('dashboard')

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