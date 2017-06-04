from django.shortcuts import render
from .models import Project
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    all_projects = Project.objects.order_by('-creation_date')
    context = {'all_projects':all_projects}
    return render(request, 'projects/projects.html', context)

def add_project(request):
    if request.method == 'GET':
        return render(request,'projects/new.html', {})
    else:
        project_name = request.POST['project_name']
        try:
            if project_name == '':
                raise Exception('Name cannot be blank')

            project = Project.objects.create(project_name=project_name, creation_date=datetime.datetime.today())
            return HttpResponseRedirect(reverse('project', args=(project.id,)))
        except Exception as e:
            return render(request, 'projects/new.html', {'error': str(e)})

def project(request, project_id):
    project = Project.objects.get(pk=project_id)
    return render(request, 'projects/project.html', {'project': project})
