from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    creation_date = models.DateField()
