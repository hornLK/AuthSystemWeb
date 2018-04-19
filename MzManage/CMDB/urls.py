from django.urls import path
from . import views
urlpatterns = [
    path('?P<^index/>',views.index),
]
