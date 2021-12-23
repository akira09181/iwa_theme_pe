from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('count',views.count,name='count'),
    path('list',views.list,name='list'),
]