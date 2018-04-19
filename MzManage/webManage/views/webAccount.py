from django.shortcuts import render,HttpResponseRedirect
from utils.login_auth import login_auth
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from webManage.forms.login_form import LoginForm
from restorage import models as restorage_model
from utils.account_auth import auth_to
import json

@csrf_exempt
def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.clean()
            email = data.get("email")
            password = data.get("password")
            authobj = auth_to(email,password)
            if authobj.auth_account():
                username,_ = email.strip().split("@")
                user = restorage_model.User.objects.get(email=email)
                ret = {"user_id":user.id,"username":username,
                       "email":email,"dept":user.dept.name,"role":user.role.name}
                request.session['auth_user'] = json.dumps(ret)
                return HttpResponseRedirect(reverse("webIndex"))
            else:
                error = "用户名或密码错误"
        login_form = LoginForm()
        return render(request,"login.html",
                      {"login_form":login_form,"error":error})
    elif request.method =="GET":
        login_form = LoginForm()
        print(request.session)
        print(request.COOKIES)
        return render(request,"login.html",{"login_form":login_form})
@login_auth
def logout(request):
    del request.session['auth_user']
    request.username = ""
    return HttpResponseRedirect(reverse("webLogin"))
