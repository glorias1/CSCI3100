from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, default='Hidden')
    date_birth = models.DateField(null=True)
    description = models.TextField(default="Leave some words to decribe youself.")
    icon = models.ImageField(null = True, blank=True)
    private = models.BooleanField(default=False)
    #image=models.ImageField()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    owner = models.ManyToManyField(User, related_name='owner')
    create_date = models.DateField('Event Date')
    members = models.ManyToManyField(User, related_name='members')
    private = models.BooleanField(default=True) ##default as private project
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name

class Announcement(models.Model):
    belong_project=models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()
    pinned = models.BooleanField(default=False)

# Create your models here.
class Budgetplan(models.Model):
    belong_project =        models.ForeignKey(Project, on_delete=models.CASCADE)

class Budget(models.Model):
    transition_id =         models.AutoField(primary_key=True)
    belong_plan =           models.ForeignKey(Budgetplan, on_delete=models.CASCADE, null=True)
    transition_category =   models.CharField(max_length=10, blank=True, null=True)  # expense/ capital
    transition_type =       models.CharField(max_length=30, blank=True, null=True)  # expense: manpower,.../ capital:caoital...
    name =                  models.CharField(max_length=50, blank=True, null=True)  # if it is capital, name='capital'
    description =           models.TextField()
    amount =                models.IntegerField(blank=True, null=True) # if it is expense, amount = negative number

    def __str__(self):
        return self.budget_transition_id

class JoinMessage(models.Model):
    pj = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    not_reply = models.BooleanField(default=True)

    def __str__(self):
        return self.message

class Tasks(models.Model):
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    start_date = models.DateField()
    due_date = models.DateField('Event Date')
    incharge = models.ManyToManyField(User)
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    finish = models.BooleanField(default=False)
    last_modify = models.DateField('Event Date')

    def __str__(self):
        return self.task_name
    
class Chat(models.Model):
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    speaker = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_date = models.DateField('Event Date')
    chat_content = models.TextField()

    def __str__(self):
        return self.belong_project

class File(models.Model):
    belong_task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    filename = models.CharField(max_length=50)
    file = models.FileField(upload_to='files')
    last_modify = models.DateField('Event Date')
    def __str__(self):
        return self.filename
