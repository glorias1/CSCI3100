from django.contrib import admin
from .models import *
# Register the models here.
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Tasks)
admin.site.register(Chat)
admin.site.register(File)