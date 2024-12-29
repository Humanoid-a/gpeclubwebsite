from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Project(models.Model):
    project_id = models.IntegerField()
    project_name = models.CharField(max_length=64)
    project_url = models.CharField(max_length=64, default='')
    project_author = models.CharField(max_length=64)
    project_version = models.CharField(max_length=32)
    #project_cover = models.ImageField(null=True, upload_to='img/')
    project_cover = models.CharField(max_length=256, default='imgs/logo.png')
    project_description = models.TextField()

class psl(models.Model):
    courses = models.CharField(max_length=256)
