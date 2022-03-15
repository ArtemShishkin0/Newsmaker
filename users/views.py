import re

from django.contrib.auth import authenticate, login, password_validation
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django_email_verification import send_email
from django.contrib.auth.models import Group, User

from NewsMaker.functions import remove_photo, is_moderator, is_ajax, match_regex, max_limit
from users.models import *
from django.contrib.auth import validators
from PIL import Image

def register(request):
    if request.method == "GET":
        context = {}
        template = loader.get_template("register.html")
        return HttpResponse(template.render(context, request))
    if request.method == "POST" and is_ajax(request):
        data = request.POST
        username = data.get("user")
        email = data.get("email")
        password = data.get("password")
        if User.objects.filter(email__exact=email):
            return JsonResponse({"error": 'This email adress is already taken'}, status=400)
        elif User.objects.filter(username__exact=username):
            return JsonResponse({"error": 'This username is already taken'}, status=400)
        else:
            if re.match(r'^[\w.@+-]+\Z', username) and 4 <= len(username) <= 20:
                pass
            else:
                return JsonResponse({"error": 'Username is invalid'}, status=400)
            if re.match(r'^(?=.*\d).{8,30}$', password):
                pass
            else:
                return JsonResponse({"error": 'Password is invalid'}, status=400)
            user = User.objects.create_user(username=username, email=email, password=password)
            Info(name=user, age=0).save()
            user.is_active = False
            user.groups.add(Group.objects.get(name='Users'))
            send_email(user)
            return JsonResponse({"success": 'User'}, status=200)
    elif request.method == "POST":
        data = request.POST
        username = data.get("user")
        email = data.get("email")
        password = data.get("password")
        if User.objects.filter(email__exact=email):
            return HttpResponse("This email is already taken")
        elif User.objects.filter(username__exact=username):
            return HttpResponse("This username is already taken")
        else:
            if re.match(r'^[\w.@+-]+\Z', username) and 4 <= len(username) <= 20:
                pass
            else:
                return HttpResponse("Invalid username")
            if re.match(r'^(?=.*\d).{8,30}$', password):
                try:
                    password_validation.validate_password(password, user=username)
                except:
                    return HttpResponse("Invalid password")
            else: return HttpResponse("Invalid password")
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
           return redirect(f"http://127.0.0.1:8000/profile/{request.user.username}")

    if request.method == "GET":
        cur_user = request.user
        req_user = User.objects.get(username=pk)
        req_user_info = Info.objects.get(name=req_user)
        if not request.user.is_anonymous:
            cur_user_info = Info.objects.get(name=cur_user)
            context = {'req_user': req_user, 'cur_user': cur_user, 'cur_user_info': cur_user_info, 'req_user_info': req_user_info , 'username': str(cur_user.username)}
        else:
            context = {'req_user': req_user, 'req_user_info': req_user_info}
        if (f"{request.path}" == f"/profile/{request.user.username}/"):
            context['profile'] =True
        template = loader.get_template("profile.html")
        return HttpResponse(template.render (context, request))

    if request.method == "POST":
        if not pk:
            pk = request.POST.get('req_username')
        if request.user != User.objects.get(username=pk): #защита от редактирования чужого профиля
            return HttpResponse(status=405)
        if is_ajax(request):
            data = request.POST
            user = User.objects.get(username=pk)
            oldpassword = data.get('oldpassword')
            newpassword = data.get('newpassword')
            confirmpassword = data.get('confirmpassword')
            if oldpassword and newpassword and confirmpassword:
                if check_password(oldpassword, user.password):
                    if newpassword == confirmpassword:
                        if newpassword == oldpassword:
                            return JsonResponse({"error": "same"}, status=400)
                        else:
                            pass
                        user.password = make_password(newpassword)
                        user.save()
                        user = authenticate(username=user.username, password=newpassword)
                        login(request, user)
                        return JsonResponse({}, status=200)
                    else:
                        return JsonResponse({"error": "match"}, status=400)
                else:
                    return JsonResponse({"error": "oldpass"}, status=400)
            else:
                return JsonResponse({"error": "Not all the fields were sent"}, status=400)

        elif request.POST.get('privacy'):
            data = request.POST
            user_info = Info.objects.get(name=request.user)
            if 'email_privacy' in data:
                user_info.show_email = True
            else:
                user_info.show_email = False
            if 'phone_privacy' in data:
                user_info.show_phone = True
            else:
                user_info.show_phone = False
            user_info.save()
        elif request.POST.get('Update'):
            data = request.POST
            fname = data.get("first_name")
            lname = data.get("last_name")
            email = data.get("email")
            phone = data.get("phone")
            age = data.get('age')
            about = data.get('about')
            if match_regex(
                fname, "^[\p{L}'][ \p{L}'-]*[\p{L}]$") and max_limit(fname, 50) and match_regex(
                lname, "^[\p{L}'][ \p{L}'-]*[\p{L}]$") and max_limit(lname, 50) and match_regex(
                phone, "^[0-9\-\+]{9,15}$") and max_limit(about, 500) and match_regex(
                email, "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"):
                pass
            else:
                return HttpResponse(status=405)
            user = User.objects.get(username=pk)
            user_info = Info.objects.get(name=request.user)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user_info.about = about

            if age != "":
                try:
                    user_info.age = int(age)
                except Exception as err:
                    pass
            else:
                user_info.age = 0
            if phone == "":
                user_info.phone = None
            else:
                user_info.phone = phone
            try:
                user.save()
                user_info.save()
            except Exception as err:
                return HttpResponse(err)
        else:
            if 'delete_photo' in request.POST:
                user_info = Info.objects.get(name=request.user)
                img = user_info.photo
                remove_photo(img)
                try:
                    img.delete(True)
                    pass
                except Exception as err:
                    print(err)
            else:
                img = request.FILES['userimg']
                try:
                    img_test = Image.open(img)
                    img_test.verify()
                    pass
                except Exception as err:
                    return HttpResponse(err)
                user_info = Info.objects.get(name=request.user)
                last_img = user_info.photo
                user_info.photo = img
                last_img_str = ''
                try:
                    last_img_str = (str(last_img).split('/')[1])
                except:

                    pass
                try:
                    user_info.save()
                    if last_img_str != str(img):
                        remove_photo(last_img)
                except Exception as err:
                    return HttpResponse(err)
        return redirect(f'http://127.0.0.1:8000/profile/{pk}')

