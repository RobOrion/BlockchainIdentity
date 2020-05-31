from django.contrib import admin
from django.urls import include, path
from home import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls', namespace='home')),
    path('login/', include('login.urls', namespace='login'))
]
