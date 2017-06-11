from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    wiki = models.CharField(max_length=100000)
    creation_date = models.DateField()
    developers = models.ManyToManyField(User)

class Discussion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    discussion_name = models.CharField(max_length=100)

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=10000)
    creation_date = models.DateField()

class File(models.Model):
    project = models.ForeignKey(Project)
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files')
    creation_date = models.DateField()
