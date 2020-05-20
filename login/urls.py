from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    path('', views.home, name='index'),
    path('process', views.custum_login, name='process'),
    path('logout', views.custum_logout, name='logout')
]
