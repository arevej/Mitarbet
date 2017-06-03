from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse 


def index(request):
    return render(request,'login/login.html', {})

def register(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html', {})
    else:
        login = request.POST['login']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.create_user(login, email, password)
            user = authenticate(username=login, password=password)
            return HttpResponseRedirect(reverse('projects'))
        except Exception as e:
            return render(request, 'registration/registration.html', { 'error': str(e) })

def projects(request):
    return render(request, 'projects/projects.html', {})
