import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Project, Discussion, Comment, File, NewsItem

def index(request):
    if 'query' in request.GET:
        q = request.GET['query']
        all_projects = Project.objects.filter(
            Q(project_name__contains=q) |
            Q(discussion__discussion_name__contains=q) |
            Q(discussion__comment__comment_text__contains=q) |
            Q(wiki__contains=q)
        ).distinct()
    else:
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
            project = Project.objects.create(project_name=project_name, creation_date=datetime.datetime.today(), wiki='')
            NewsItem.objects.create(user=request.user, creation_date=datetime.datetime.today(), project=project, action='create_project')
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

def edit_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    all_developers = User.objects.exclude(project__id=project_id)
    if request.method == "GET":
        return render(request, 'projects/edit.html', {'project': project, 'all_developers': all_developers})
    else:
        wiki = request.POST['wiki']
        project.wiki=wiki
        project.save()
        return HttpResponseRedirect(reverse('project', args=(project.id,)))

def add_developer(request, project_id):
    project = Project.objects.get(pk=project_id)
    developer_id = request.POST['developer_id']
    developer = User.objects.get(pk=developer_id)
    project.developers.add(developer)
    return HttpResponseRedirect(reverse('edit_project', args=(project.id,)))

def delete_developer(request, project_id, developer_id):
    project = Project.objects.get(pk=project_id)
    developer = User.objects.get(pk=developer_id)
    project.developers.remove(developer)
    return HttpResponseRedirect(reverse('edit_project', args=(project.id,)))

def add_file(request, project_id):
    project = Project.objects.get(pk=project_id)
    file = request.FILES['file']
    file_name = request.POST['file_name']
    if file_name == '':
        return HttpResponseRedirect(reverse('project', args=(project.id,)))
    project.file_set.create(file=file, file_name=file_name, creation_date=datetime.datetime.today())
    return HttpResponseRedirect(reverse('project', args=(project.id,)))

def delete_file(request, project_id, file_id):
    project = Project.objects.get(pk=project_id)
    file = File.objects.get(pk=file_id)
    file.delete()
    return HttpResponseRedirect(reverse('project', args=(project.id,)))

def news(request):
    news = NewsItem.objects.order_by('-creation_date')
    return render(request, 'news/news.html', {'news':news})
