from django.shortcuts import render
from .models import Project 

def index(request):
    all_projects = Project.objects.order_by('-creation_date')
    context = {'all_projects':all_projects}
    return render(request, 'projects/projects.html', context)
