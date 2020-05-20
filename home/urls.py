from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='index'),
    path('profile', views.profile, name='profile'),
    path('permpre', views.permpre, name='permpre'),
    path('permperso', views.permperso, name='permpre'),

]
