import json

import requests
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from BlockChainIdentity import settings
from blockchain.POC import Blockchain
from django.contrib.auth.models import Group, User
from home.models import Demande


# Create your views here.


@login_required()
def home(request):
    if is_admin(request):
        id_user = request.user.id
    else:
        id_user = ""
    return render(request, 'home/succeed.html', {'nbr_request': get_nbr_demande(id_user)})


@login_required()
def profile(request):
    if is_admin(request):
        id_user = request.user.id
    else:
        id_user = ""
    return render(request, 'home/profile.html', {'user': request.user, 'nbr_request': get_nbr_demande(id_user)})


@login_required()
def demand(request):
    if is_admin(request):
        id_user = request.user.id
        all_demand = get_all_id_demand(id_user)
        return render(request, 'home/demand.html', {
            'user': request.user,
            'nbr_request': get_nbr_demande(id_user),
            'demand': all_demand
        })
    else:
        id_user = ""
    return render(request, 'home/profile.html', {'user': request.user})


def adduser(request):
    if is_admin(request):
        id_user = request.user.id
        return render(request, 'home/adduser.html', {'user': request.user, 'nbr_request': get_nbr_demande(id_user)})
    else:
        id_user = ""
    return render(request, 'home/profile.html', {'user': request.user})


def accept_demand(request):
    if is_admin(request):
        id_user = request.user.id
        id_demand = request.POST.get("id_demand")
        demande_tmp = Demande.objects.get(id=id_demand)
        demande_tmp.validators = demande_tmp.validators + " " + str(request.user.id)
        demande_tmp.save()
        demande_check = Demande.objects.get(id=id_demand)
        if len(demande_tmp.validators.split(" ")) - 1 == len_users_admin():
            test_user_after(request, demande_check.value)
            demande_check.delete()
        return render(request, 'home/adduser.html', {'user': request.user, 'nbr_request': get_nbr_demande(id_user)})
    else:
        id_user = ""
    return render(request, 'home/profile.html', {'user': request.user})


def deny_demand(request):
    if is_admin(request):
        id_user = request.user.id
        id_demand = request.POST.get("id_demand")
        demande_tmp = Demande.objects.get(id=id_demand)
        demande_tmp.delete()
        return render(request, 'home/adduser.html', {'user': request.user, 'nbr_request': get_nbr_demande(id_user)})
    else:
        id_user = ""
    return render(request, 'home/profile.html', {'user': request.user})


@login_required()
def permpre(request):
    if is_admin(request):
        id_user = request.user.id
    else:
        id_user = ""
    first_name = request.POST.get("user").split(' ')[0]
    last_name = request.POST.get("user").split(' ')[1]
    user_tmp = User.objects.get(first_name=first_name, last_name=last_name)
    user = {
        # 'lastname': user_tmp.last_name,
        # 'firstname': user_tmp.first_name,
        'email': user_tmp.email,
        'rights': request.POST.get("permission_pre")
    }
    requests.post(
        f'http://localhost:5000/transaction/insert',
        json=user
    )
    return render(request, 'home/profile.html', {'user': request.user, 'nbr_request': get_nbr_demande(id_user)})


@login_required()
def permperso(request):
    if is_admin(request):
        id_user = request.user.id
    else:
        id_user = ""
    first_name = request.POST.get("user").split(' ')[0]
    last_name = request.POST.get("user").split(' ')[1]
    user_tmp = User.objects.get(first_name=first_name, last_name=last_name)
    user = {
        # 'lastname': user_tmp.last_name,
        # 'firstname': user_tmp.first_name,
        'email': user_tmp.email,
        'rights': request.POST.get("permission_perso")
    }
    requests.post(
        f'http://localhost:5000/transaction/insert',
        json=user
    )
    return render(request, 'home/profile.html', {'user': request.user, 'nbr_request': get_nbr_demande(id_user)})


@login_required()
def test_user_before(request):
    if is_admin(request):
        id_user = request.user.id
    else:
        id_user = ""
    name = request.POST.get("nom")
    firsname = request.POST.get("prenom")
    email = request.POST.get("email")
    user = {
        'name': name,
        'firstname': firsname,
        'email': email,
        'rights': []
    }

    obj = Demande.objects.create(value=json.dumps(user), validators="")
    obj.save()
    users_in_group = Group.objects.get(name="admin").user_set.all()
    users = listuser_mail(users_in_group)
    tmp_user = request.user.first_name + " " + request.user.last_name
    if tmp_user in listuser(users_in_group):
        send_emails(users)

    return render(request, 'home/profile.html', {'user': request.user, 'nbr_request': get_nbr_demande(id_user)})


def test_user_after(request, data):
    if is_admin(request):
        id_user = request.user.id
    else:
        id_user = ""
    print(data)
    user = json.loads(data)
    requests.post(
        f'http://localhost:5000/transaction/create',
        json=user
    )

    return render(request, 'home/profile.html', {'user': request.user, 'nbr_request': get_nbr_demande(id_user)})




def listuser(query):
    user = []
    for u in query:
        user.append(u.first_name + " " + u.last_name)
    return user


def listuser_mail(query):
    user = []
    for u in query:
        user.append(u.email)
    return user


def send_emails(list_mail):
    subject = 'Blockchain nouveau block'
    message = 'Un nouveau block est apparu merci de le vérfier sur votre espace personnel ' \
              ': http://localhost:8000/home/profile'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = list_mail
    send_mail(subject, message, email_from, recipient_list)


def get_nbr_demande(id_user):
    i = 0
    for d in list(Demande.objects.all()):
        if str(id_user) not in d.validators:
            i = i + 1
    return i


def get_all_id_demand(id_user):
    list_demand = []
    for d in list(Demande.objects.all()):
        if str(id_user) not in d.validators:
            list_demand.append(d)
    return list_demand


def is_admin(user_given):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    print(listuser(users_in_group))
    tmp_user = user_given.user.first_name + " " + user_given.user.last_name
    return tmp_user in listuser(users_in_group)


def len_users_admin():
    return len(Group.objects.get(name="admin").user_set.all())
