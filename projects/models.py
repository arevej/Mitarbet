from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    wiki = models.CharField(max_length=100000, default='')
    creation_date = models.DateField()
    developers = models.ManyToManyField(User)
    tags = models.CharField(max_length=1000, default='')

    def tag_list(self):
        return self.tags.split(' ')

    @staticmethod
    def all_tags():
        all_tags = []
        for project in list(Project.objects.all()):
            for tag in project.tag_list():
                if (tag in all_tags) == False:
                    all_tags.append(tag)
        return all_tags

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

class NewsItem(models.Model):
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField()
    project = models.ForeignKey(Project)
    action = models.CharField(max_length=50) # create_project
