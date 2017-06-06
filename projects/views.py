from django.shortcuts import render
from .models import Project, Discussion, Comment
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

def discussion_list(request, project_id):
    project = Project.objects.get(pk=project_id)
    all_discussions = project.discussion_set.all()
    return render(request, 'discussions/discussions.html', {'project':project,'all_discussions':all_discussions})

def add_discussion(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == "GET":
        return render(request, 'discussions/new.html', {'project':project})
    else:
        discussion_name = request.POST['discussion_name']
        try:
            if discussion_name == '':
                raise Exception('Name cannot be blank')
            discussion = project.discussion_set.create(discussion_name=discussion_name)
            return HttpResponseRedirect(reverse('discussion_list', args=(project.id,)))
        except Exception as e:
            return render(request, 'discussions/new.html', {'error': str(e), 'project':project})

def discussion(request, project_id, discussion_id):
    project = Project.objects.get(pk=project_id)
    discussion = Discussion.objects.get(pk=discussion_id)
    return render(request, 'discussions/discussion.html', {'project': project, 'discussion': discussion})

def comment(request, project_id, discussion_id):
    project = Project.objects.get(pk=project_id)
    discussion = Discussion.objects.get(pk=discussion_id)
    user = request.user
    comment_text = request.POST['comment_text']
    discussion.comment_set.create(comment_text=comment_text, creation_date=datetime.datetime.today(), user=user)
    return HttpResponseRedirect(reverse('discussion', args=(project.id,discussion_id)))
