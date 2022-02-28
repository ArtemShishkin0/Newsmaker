from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django_email_verification import send_email
from django.contrib.auth.models import Group, User
from users.models import *

def register(request):
    if request.method == "GET":
        context = {}
        template = loader.get_template("register.html")
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        data = request.POST
        username = data.get("user")
        email = data.get("email")
        password = data.get("password")
        if User.objects.filter(email__exact=email):
            return HttpResponse("This email is already taken")
        elif User.objects.filter(username__exact=username):
            return HttpResponse("This username is already taken")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Info(name=user, age=0).save()
            user.is_active = False
            user.groups.add(Group.objects.get(name='Users'))
            send_email(user)
            return HttpResponse("Check your email.")


def profile(request, pk=None):
    if request.method == "GET" and request.path == "/profile/":
        if request.user.is_anonymous:
            return redirect("http://127.0.0.1:8000/login/?next=/profile/")      #имитация декоратора login_required для своего профиля
        else:
       # if redirect_to_profile(request):
           return redirect(f"http://127.0.0.1:8000/profile/{request.user.username}")

    if request.method == "GET":
        cur_user = request.user
        req_user = User.objects.get(username=pk)
        req_user_info = Info.objects.get(name=req_user)
        if not request.user.is_anonymous:
            cur_user_info = Info.objects.get(name=cur_user)
            context = {'req_user': req_user, 'cur_user': cur_user, 'cur_user_info': cur_user_info, 'req_user_info': req_user_info }
        else:
            context = {'req_user': req_user, 'req_user_info': req_user_info}
        template = loader.get_template("profile.html")

        return HttpResponse(template.render (context, request))
    if request.method == "POST":
        if request.POST.get('password'):
            data = request.POST
            user = User.objects.get(username=pk)
            oldpassword = data.get('oldpassword')
            newpassword = data.get('newpassword')
            confirmpassword = data.get('confirmpassword')
            if oldpassword and newpassword and confirmpassword:
                if check_password(oldpassword, user.password):
                    if newpassword == confirmpassword:
                        user.password = make_password(newpassword)
                        user.save()
                        user = authenticate(username=user.username, password=newpassword)
                        login(request, user)
                        print("password updated")
                    else:
                        print("passwords do not match")
                else:
                    print("wrong old password")

        elif request.POST.get('privacy'):
            data = request.POST
            user_info = Info.objects.get(name=request.user)
            print(data)
            if 'email_privacy' in data:
                user_info.show_email = True
            else:
                user_info.show_email = False
            if 'phone_privacy' in data:
                user_info.show_phone = True
            else:
                user_info.show_phone = False
            user_info.save()
        else:       #обработать конкретную форму
            data = request.POST

            user = User.objects.get(username=pk)
            user_info = Info.objects.get(name=request.user)
            user.first_name = data.get("first_name")
            user.last_name = data.get("last_name")
            user.email = data.get("email")
            if data.get('age') != "":
                try:
                    age = int(data.get('age'))
                    user_info.age = data.get('age')
                except Exception as err:
                    pass
            else:
                user_info.age = 0
            if data.get('phone') == "":
                user_info.phone = None    #сделать не none а именно null
            else:
                user_info.phone = data.get('phone')
            user_info.about = data.get('about')
            try:
                user.save()
                user_info.save()
            except Exception as err:
                return HttpResponse(err)
        return redirect(f'http://127.0.0.1:8000/profile/{pk}')

def is_moderator(user):
    return user.groups.filter(name='Moderators').exists()

