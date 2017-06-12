from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from projects.models import Project


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

def profile(request, username):
    user = User.objects.get(username=username)
    projects = Project.objects.filter(developers__id=user.id)
    return render(request, 'profile/profile.html',{'user': user, 'projects':projects})

def edit_profile(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'profile/edit.html', {'user': user})
    else:
        if 'avatar' in request.FILES:
            user.profile.avatar = request.FILES['avatar']
        user.profile.style = request.POST['style']
        user.profile.save()
        return HttpResponseRedirect(reverse('profile', args=(user.username,)))
