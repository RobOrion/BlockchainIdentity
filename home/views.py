from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def home(request):
    return render(request, 'home/succeed.html')


@login_required()
def profile(request):
    return render(request, 'home/profile.html', {'user': request.user})


@login_required()
def permpre(request):
    print(request.POST.get("user"))
    print(request.POST.get("permission_pre"))
    return render(request, 'home/profile.html', {'user': request.user})


@login_required()
def permperso(request):
    print(request.POST.get("user"))
    print(request.POST.get("permission_perso"))
    return render(request, 'home/profile.html', {'user': request.user})
