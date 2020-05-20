from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, 'login/home.html')


def custum_login(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username)
    print(password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'home/succeed.html', {'message': 'login'})
    else:
        return render(request, 'login/home.html', {'message': 'error'})


def custum_logout(request):
    logout(request)
    return render(request, 'login/home.html', {'message': 'logout'})
