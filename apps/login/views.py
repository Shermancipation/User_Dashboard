from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages

def index(request):
    return render(request, "login/signin.html")

def register(request):
    return render(request, "login/register.html")

def userpage(request):
    request.session['loggedin'] == "User"
    all_users = User.objects.get_users()
    context = {
        'users': all_users
    }
    return render(request, "login/userpage.html", context)


def adminpage(request):
    request.session['loggedin'] == "Admin"
    all_users = User.objects.get_users()
    context = {
        'users': all_users
    }
    return render(request, "login/adminpage.html", context)

def create_user(request):
    if request.method=="POST":
        response_from_models = User.objects.user_validation(request.POST)
        if response_from_models['status']:
            if response_from_models['user'].admin == True:
                request.session['loggedin'] = "Admin"
            else:
                request.session['loggedin'] = "User"
            request.session["id"] = response_from_models["user"].id
            pass
        else:
            request.session['error_group'] = True
            for i in response_from_models["error"]:
                messages.error(request, i)
            return redirect('/')
    else:
        return redirect('/')
    if request.session['loggedin'] == "Admin":
        return redirect('login:admin')
    if request.session['loggedin'] == "User":
        return redirect('login:user')

def remove_user(request, id):
    User.objects.remove_user(id)
    return redirect('login:admin')

def login(request):
    if request.method=="POST":
        response_from_models = User.objects.login_validation(request.POST)
        if response_from_models['status']:
            if response_from_models['user'].admin == True:
                request.session['loggedin'] = "Admin"
            else:
                request.session['loggedin'] = "User"
            request.session["id"] = response_from_models["user"].id
            pass
        else:
            request.session['error_group'] = False
            for i in response_from_models["errors"]:
                messages.error(request, i)
            return redirect('/')
    else:
        return redirect('/')
    if request.session['loggedin'] == "Admin":
        return redirect('login:admin')
    if request.session['loggedin'] == "User":
        return redirect('login:user')

def logout(request):
    request.session.flush()
    return redirect('/')
