from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from utils.request_api import secret_apirequest
from django.views.decorators.csrf import csrf_exempt
from fortress.form import AddUserForm
import requests,json
from utils.login_auth import login_auth

# Create your views here.
#授权管理主页

@login_auth
@csrf_exempt
def index(request):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    adduser_form = AddUserForm()
    try:
        if request.method == "POST":
            adduser_form = AddUserForm(request.POST)
            if adduser_form.is_valid():
                cd = adduser_form.cleaned_data
                int(cd.get("phonenumber"))
                cd["username"] = cd.get("email").strip().split("@")[0].replace(".","_")
                adduser_url = settings.AUTHS_URL+"/apiv1/auths/user/create/"
                result = requests.post(adduser_url,headers=headers,data=json.dumps(cd)).text
            return HttpResponseRedirect(reverse("auths_index"))

        elif request.method == "GET":
            page = request.GET.get("page",1)
            userlist_url = settings.AUTHS_URL+"/apiv1/auths/user/page/list/"
            hostlist_url = settings.AUTHS_URL+"/apiv1/auths/host/page/list/"
            rolelist_url = settings.AUTHS_URL+"/apiv1/auths/role/list/"
            aduitusers = json.loads(requests.get(userlist_url,headers=headers,params={"page":int(page)}).text)
            aduithosts = json.loads(requests.get(hostlist_url,headers=headers).text)
            aduitroles = json.loads(requests.get(rolelist_url,headers=headers).text)
            data ={"aduitusersinfo":aduitusers,
                   "aduithostscount":aduithosts.get("count",0),
                 "aduitroles":aduitroles
                }
            return render(request,"authManager/index.html",
                          {"data":data,"addUserForm":adduser_form,"status":True}
                         )

    except Exception  as e:
        print(e)
        data = {}
        return HttpResponseRedirect(reverse("auths_index"))

@csrf_exempt
def delUserHost(request):
    if request.method == "POST":
        ajax_data=request.POST.get("data")
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        deluserhost_url = settings.AUTHS_URL+"/apiv1/auths/user/delhost/"
        result = requests.post(deluserhost_url,headers=headers,data=ajax_data).text
        return HttpResponse(result,content_type="application/json")
#index界面中编辑用户信息的按钮
@csrf_exempt
def authorizeEditUser(request):
    if request.method == "POST":
        ajax_data=request.POST.get("data")
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        useredit_url = settings.AUTHS_URL+"/apiv1/auths/user/edit/"
        result = requests.post(useredit_url,headers=headers,data=ajax_data).text
        return HttpResponse(result,content_type="application/json")
    else:

        return HttpResponse(json.dumps({"status":False,"message":"method error"}),
                            content_type="application/json")
#获取登录角色
@csrf_exempt
def authorizeGetRoles(request):
    if request.method == "GET":
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        try:
            role_url = settings.AUTHS_URL+"/apiv1/auths/role/list/"
            role_list = requests.get(role_url,headers=headers).text
            return HttpResponse(role_list,content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status":False,"message":e}),
                                            content_type="application/json")
#编辑保存角色
@csrf_exempt
def authorizeEditUserRole(request):
    if request.method == "POST":
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        ajax_data=request.POST.get("data")
        userroleedit_url = settings.AUTHS_URL+"/apiv1/auths/userrole/edit/"
        result = requests.post(userroleedit_url,headers=headers,data=ajax_data).text
        return HttpResponse(result,content_type="application/json")
#为用户添加主机访问权限
@csrf_exempt
def authorizeAddUserRole(request,user_id):
    try:
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        page = request.GET.get("page",1)
        authuser_url = settings.AUTHS_URL+"/apiv1/auths/user/info/"
        outhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/page/out-list/"
        role_url = settings.AUTHS_URL+"/apiv1/auths/role/list/"
        user_res = json.loads(requests.get(authuser_url,headers=headers,params={"user_id":user_id}).text)
        out_hosts = json.loads(requests.get(outhosts_url,headers=headers,params={"user_id":user_id,"page":int(page)}).text)
        role = json.loads(requests.get(role_url,headers=headers).text)
        data = {
                    "hosts_info":out_hosts,
                    "user_info":user_res.get("user_info"),
                    "role_info":role
                }
        return render(request,"authManager/authorizeAddUserRole.html",
                      {"data":data,"status":True})
    except Exception as e:
        print(e)
        return render(request,"authManager/authorizeAddUserRole.html")

#管理用户登录权限
def authorizeUser(request,user_id):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    try:
        page = request.GET.get("page",1)
        authuser_url = settings.AUTHS_URL+"/apiv1/auths/user/info/"
        userhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/page/list/"
        user_res = json.loads(requests.get(authuser_url,headers=headers,params={"user_id":user_id}).text)
        userhosts_res = json.loads(requests.get(userhosts_url,headers=headers,params={"user_id":user_id,"page":int(page)}).text)
        data = {
                "user_hosts":userhosts_res,
                "user_info":user_res.get("user_info")
            }
        return render(request,"authManager/authorizeUser.html",{
            "data":data,"status":True
        })
    except Exception as e:
        print(e)
        return render(request,"authManager/authorizeUser.html")

#ajax分页获取不属于用户的机器
def authorizeUserOutHosts(request,user_id):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    try:
        if request.method == "GET":
            page = request.GET.get("page",1)
            outhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/page/out-list/"
            out_hosts = requests.get(outhosts_url,headers=headers,params={"user_id":user_id,"page":int(page)}).text
            return HttpResponse(out_hosts,content_type="application/json")
    except Exception as e:
        print(e)
        return HttpResponse({"status":False},content_type="application/json")

#ajax添加用户主机授权
@csrf_exempt
def authorizeAuthHostsUser(request):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    try:
        if request.method == "POST":
            data = request.POST.get("data")
            authhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/authshosts/"
            res = requests.post(authhosts_url,headers=headers,data=data).text
            return HttpResponse({"status":res},content_type="application/json")
    except Exception as e:
            return HttpResponse({"status":res},content_type="application/json")
