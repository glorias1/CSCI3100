from django.db import models

# Create your models here.
class userAccount(models.Model):
    username = models.CharField(max_length=30,default='',unique=True)
    email = models.CharField(max_length=255,default='',unique=True)
    password = models.CharField(max_length=16, default='')
    def __str__(self):
        return self.username + self.email