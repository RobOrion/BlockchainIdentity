from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='index'),
    path('profile', views.profile, name='profile'),
    path('permpre', views.permpre, name='permpre'),
    path('permperso', views.permperso, name='permpre'),
    path('testuser', views.test_user_before, name='testuser'),
    path('adduser', views.adduser, name='adduser'),
    path('demand', views.demand, name='demand'),
    path('accept_demand', views.accept_demand, name='accept_demand'),
    path('deny_demand', views.deny_demand, name='deny_demand'),

]
