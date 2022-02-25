import random
import hashlib
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.core.mail import send_mail
from articles.models import *
from django.contrib.auth.models import Group, User
from users.models import *


#
# def home(request):
#     context = {'is_moderator': is_moderator}
#     template = loader.get_template("main.html")
#     return HttpResponse(template.render(context, request))


def login_view(request):
    if request.method == "GET":
        context = {}
        template = loader.get_template("login.html")
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        data = request.POST
        username = data.get("user")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    return redirect(request.GET.get('next'))
                except:
                    return redirect('/home')
            else:
                return HttpResponse("Account is deactivated")
        else:
            return HttpResponse("Invalid login data")

def logout_view(request):
    logout(request)
    return redirect('/home')
