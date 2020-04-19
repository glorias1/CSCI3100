from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    owner = models.ManyToManyField(User, related_name='owner')
    create_date = models.DateField('Event Date')
    members = models.ManyToManyField(User, related_name='members')
    closed = models.BooleanField(default=False)

class Tasks(models.Model):
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    due_date = models.DateField('Event Date')
    incharge = models.ManyToManyField(User)
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    finish = models.BooleanField(default=False)
    last_modify = models.DateField('Event Date')
    
class Chat(models.Model):
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    speaker = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_date = models.DateField('Event Date')
    chat_content = models.TextField()

class File(models.Model):
    belong_task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    filename = models.CharField(max_length=50)
    file = models.FileField(upload_to='files')