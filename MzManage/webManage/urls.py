from django.urls import path,re_path
from webManage.views import webIndex,webAccount
urlpatterns = [
    re_path(r'^$',webIndex.index,name="webIndex"),
    re_path(r'^login/',webAccount.login,name="webLogin"),
    re_path(r'^logout/',webAccount.logout,name="webLogout"),
]
