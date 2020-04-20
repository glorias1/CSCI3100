from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User_Privacy)
admin.site.register(Project)
admin.site.register(Tasks)
admin.site.register(Chat)
admin.site.register(File)