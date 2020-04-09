from django.db import models

# Create your models here.
class usertable(models.Model):
    username = models.CharField(max_length=30,default='')
    email = models.CharField(max_length=255,default='')
    password = models.CharField(max_length=16, default='')
    def __str__(self):
        return self.username + self.email