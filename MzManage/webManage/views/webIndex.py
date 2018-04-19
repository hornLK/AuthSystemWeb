from django.shortcuts import render,HttpResponseRedirect
from utils.login_auth import login_auth

@login_auth
def index(request):
    return render(request,"index.html")

