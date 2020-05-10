"""MapOut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, login
from mapout_app.views import *
from django.views.generic.base import RedirectView

urlpatterns = [
    re_path(r'^project/(?P<id1>\d+)/addbudget/', create_budget, name='createbudget'),         ##budget plans
    re_path(r'^project/(?P<id1>\d+)/addbudget2/', create_budget_2, name='createbudget2'),     ##budget plans
    re_path(r'^project/(?P<id3>\d+)/viewplan/', view_budget, name='viewbudget'),    ## view budget
    
    path('admin/', admin.site.urls),                            ##admin page
    path('home/', home, name='home'),                           ##home page before log in
    path('', RedirectView.as_view(url='/home/')),              ##redirect to /home/ if empty url
    path('accounts/', include('django.contrib.auth.urls')),     ##for account use(no .html return)
    path('accounts/login/', login_view1, name='login'),         ##page for login 
    #path('accounts/reset-password', pw_enter, name='password_reset'), ##input email to reset password
    #path('accounts/email-sent', )
    #path('accounts/login/password_reset_confirm', pw_con, name='password_reset_confirm'),
    #path('accounts/login/reset', reset_confirmed, name='password_reset_confirm'), #jump to reset page
    path('accounts/signup/', signup_view, name='signup'),       ##page for sign up (maybe can add email verrification if have time)
    path('logout/', logout1),                                   ##url of logout
    path('index/', index, name='index'),                        ##home page, user can see their nearest dueing task or other things
    path('projects/',index_projects, name='index_projects'),    ##overview of all projects, user can click on one of the project(card) to enter the detailed project page
    path('tasks/', index_tasks, name='index_tasks'),            ##overview of all tasks, user can click on one of the task(card) to enter the detailed task page
    path('help/', help_, name='help'),                          ##FAQ page
    path('schedule/', schedule, name='schedule'),               ##showing the calendar of this month(?) and tasks are list on there
    path('settings/', settings_, name='settings'),              ##change settings
    path('createproject', create_project, name='createproject'),        ##user enter project name and description to create a new project
    path('createtask', create_task, name='createtask'),                 ##user enter task name and description and due date to create a new task
    re_path(r'^project/(?P<id>\d+)/$', view_project, name='viewproject'),       ##dynamic detailed page of a project, have chatroom and list of task, team leader can close/delete the project, add new members and add team leader 
    re_path(r'^project/(?P<id1>\d+)/task/(?P<id2>\d+)/$', view_task, name='viewtask'),       ##dynamic detailed page of a task, can upload file and delete file and download file, user can set the task as finished
    
    #re_path(r'^projects/join/(?P<pid>\d+)/$', join_project, name='join_project'),
    path('allpublicuser/', allpublicuser, name='allpublicuser'),
    re_path(r'^allpublicuser/(?P<id>\d+)/$', viewprofile, name='viewprofile'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
