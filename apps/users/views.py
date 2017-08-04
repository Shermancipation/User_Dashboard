from django.shortcuts import render, redirect, HttpResponse
from ..login.models import User
from .models import Message
from .models import Comment
from django.contrib import messages
from django.core.urlresolvers import reverse

def newUserPage(request):
    return render(request, 'users/newUserPage.html')

def createNewUser(request):
    if request.method=="POST":
        response_from_models = User.objects.user_validation(request.POST)
        if response_from_models['status']:
            return redirect('login:admin')
        else:
            request.session['error_group'] = True
            for error in response_from_models["error"]:
                messages.error(request, error)
            return redirect('users:newUserPage')
    else:
        return redirect('users:newUserPage')

def edit_user(request):
    if request.method=="POST":
        user = User.objects.get(id=request.session['editUserId'])
        response_from_models = User.objects.edit_validation(request.POST, user)
        if response_from_models['status']:
            return redirect('login:admin')
        else:
            request.session['error_group'] = True
            for error in response_from_models["error"]:
                messages.error(request, error)
            return redirect('login:admin')
    else:
        return redirect('login:admin')

def edit_password(request):
    if request.method=="POST":
        user = User.objects.get(id=request.session['editUserId'])
        response_from_models = User.objects.password_edit_validation(request.POST, user)
        if response_from_models['status']:
            return redirect('login:admin')
        else:
            request.session['error_group'] = True
            for error in response_from_models["error"]:
                messages.error(request, error)
            return redirect('login:admin')
    else:
        return redirect('login:admin')

def edit_profile(request):
    if request.method=="POST":
        user = User.objects.get(id=request.session['id'])
        response_from_models = User.objects.edit_profile(request.POST, user)
        if response_from_models['status']:
            return redirect('login:user')
        else:
            request.session['error_group'] = True
            for error in response_from_models["error"]:
                messages.error(request, error)
            return redirect('login:user')
    else:
        return redirect('login:admin')

def edit_user_password(request):
    if request.method=="POST":
        user = User.objects.get(id=request.session['id'])
        response_from_models = User.objects.edit_user_password(request.POST, user)
        if response_from_models['status']:
            return redirect('login:user')
        else:
            request.session['error_group'] = True
            for error in response_from_models["error"]:
                messages.error(request, error)
            return redirect('login:user')
    else:
        return redirect('login:admin')

def edit_description(request):
    if request.method=="POST":
        user = User.objects.get(id=request.session['id'])
        response_from_models = User.objects.edit_description(request.POST, user)
        return redirect('login:user')
    else:
        return redirect('login:admin')

def editUserPage(request, id):
    request.session['editUserId'] = id
    user = User.objects.get(id=id)
    context = {
        "user": user
    }
    return render(request, "users/editUserPage.html", context)

def userEditUserPage(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, "users/userEditUserPage.html", context)

def showUserPage(request, id):
    request.session['showUserId'] = id
    user = User.objects.get(id=id)
    try:
        messages = Message.objects.filter(user=user)
    except:
        messages = None
    print(messages)
    context = {
        "user": user,
        "messages": messages
    }
    return render(request, "users/showUserPage.html", context)

def postMessage(request):
    if request.method=="POST":
        messageReceiver = User.objects.get(id=request.session['showUserId'])
        loggedUser = User.objects.get(id=request.session['id'])
        response_from_models = Message.objects.post_message(request.POST, messageReceiver, loggedUser)
        if response_from_models['status']:
            return redirect(reverse('users:showUserPage', kwargs={'id': request.session['showUserId']}))
        else:
            request.session['error_group'] = True
            for error in response_from_models["error"]:
                messages.error(request, error)
            return redirect(reverse('users:showUserPage', kwargs={'id': request.session['showUserId']}))
    else:
        return redirect(reverse('users:showUserPage', kwargs={'id': request.session['showUserId']}))

def postComment(request, messageId):
    if request.method=="POST":
        commentReceiver = User.objects.get(id=request.session['showUserId'])
        loggedUser = User.objects.get(id=request.session['id'])
        currentMessage = Message.objects.get(id=messageId)
        response_from_models = Comment.objects.post_comment(request.POST, commentReceiver, loggedUser, currentMessage)
        if response_from_models['status']:
            return redirect(reverse('users:showUserPage', kwargs={'id': request.session['showUserId']}))
        else:
            request.session['error_group'] = True
            for error in response_from_models["error"]:
                messages.error(request, error)
            return redirect(reverse('users:showUserPage', kwargs={'id': request.session['showUserId']}))
    else:
        return redirect(reverse('users:showUserPage', kwargs={'id': request.session['showUserId']}))
