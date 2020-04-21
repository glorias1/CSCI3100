from django.http import HttpResponseRedirect, FileResponse, StreamingHttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from .forms import *
from .models import *
import time
import os

def index_budgets(request):
    return render(request, 'budget/index.html')

def create_budget(request):
    if request.method == 'POST':
        transition_capital =            Budget()
        transition_capital.name =       "capital"
        transition_capital.amount =     request.POST.get('capital')
        transition_capital.save()

        transition_expense_1 =          Budget()
        transition_expense_1.name =     request.POST.get('expense_1_name')
        amount =                        request.POST.get('expense_1_amount') * 1
        transition_expense_1.amount =   amount
        transition_expense_1.save()

        transition_expense_2 =          Budget()
        transition_expense_2.name =     request.POST.get('expense_2_name')
        amount =                        request.POST.get('expense_2_amount') * 1
        transition_expense_2.amount =   amount
        transition_expense_2.save()

        transition_expense_3 =          Budget()
        transition_expense_3.name =     request.POST.get('expense_3_name')
        amount =                        request.POST.get('expense_3_amount') * 1
        transition_expense_3.amount =   amount
        transition_expense_3.save()

        return render(request, 'budget/create_plan.html', {'form': [transition_capital]})
    return render(request, 'budget/create_plan.html')

def home(request):
    return render(request, 'home.html')

def index(request):
    if not request.user.is_authenticated:
        not_loggedin = True
        context = {'not_loggedin':not_loggedin}
        return render(request, 'main.html', context)
    else:
        myprojects = Project.objects.filter(members = request.user, closed = False)
        mytasks = Tasks.objects.filter(incharge=request.user).order_by('due_date')
        context = {'mytasks':mytasks, 'myprojects':myprojects}
        return render(request, 'main.html', context)

def index_projects(request):
    #get the projects involed by the current user
    projects = Project.objects.filter(members = request.user).order_by('closed')
    all_public_project = Project.objects.filter(private = False).order_by('project_name')
    tasks = Tasks.objects.filter(belong_project__in = projects)  ##filter all the task in the list of project objects
    context = {'projects':projects, 'tasks':tasks, 'all_public_project': all_public_project}
    return render(request, 'main_projects.html', context)

def index_tasks(request):
    tasks = Tasks.objects.filter(incharge = request.user).order_by('finish')
    context = {'tasks':tasks}
    return render(request, 'main_tasks.html', context)

def login_btn(request):
    return render(request, 'registration/login.html')

def login_view1(request):
    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/index/')
    elif request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return HttpResponseRedirect("request.path_info")
            #return redirect('index.html')
        else:
            return render_to_response('home.html')

def logout1(request):
    logout(request)
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.private = form.cleaned_data.get('privacy')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def schedule(request):
    return  render(request, 'schedule.html')

def help_(request):
    return  render(request, 'help.html')

def settings_(request):
    return  render(request, 'settings.html')

def create_project(request):
    createproject = Project()
    if request.method == 'POST':
        if request.POST.get('project_name') and request.POST.get('project_description'):
            createproject.project_name = request.POST.get('project_name')
            createproject.project_description = request.POST.get('project_description')
            createproject.private = request.POST.get('project_privacy')
            createproject.create_date = datetime.now()
            createproject.save()
            createproject.owner.add(request.user)    ##add current usre as owner
            createproject.members.add(request.user)   ##add current user as a member
            messages.success(request, 'You have successfully created a project.')
            return HttpResponseRedirect(reverse('viewproject', args=[createproject.id]))
    return render(request, 'create_project.html')


def create_task(request):
    ##send the list of projects 
    projects = Project.objects.filter(members = request.user)
    options = {'projects':projects}
    createtask = Tasks()
    if request.method == 'POST':
        if request.POST.get('task_name') and request.POST.get('belong_project_select'):
            createtask.task_name = request.POST.get('task_name')
            createtask.last_modify = datetime.now()
            selected_project_id = request.POST.get('belong_project_select')
            createtask.belong_project = Project.objects.get(id = selected_project_id)
            if request.POST.get('due_date'):
                createtask.due_date = request.POST.get('due_date')
            if request.POST.get('task_description'):
                createtask.task_description = request.POST.get('task_description')
            createtask.save()
            createtask.incharge.add(request.user)
            return HttpResponseRedirect(reverse('viewtask', args=[createtask.belong_project.id,createtask.id]))
    return render(request, 'create_task.html', options)

def view_project(request, id):
    ##see the detail page of a project
    viewing_project = Project.objects.get(id=id)
    tasks = Tasks.objects.filter(belong_project = viewing_project)
    all_leaders = viewing_project.owner.all()
    project_members = viewing_project.members.all()
    project_leader = viewing_project.owner.all()
    project_members_not_owner = viewing_project.members.exclude(id__in = project_leader)
    msgs = Chat.objects.filter(belong_project = viewing_project).order_by('sent_date')
    ## see if the request user is the owner of the project
    try:
        if viewing_project.owner.get(id = request.user.id):
            is_owner = True
    except:
        is_owner = False
    try:
        if viewing_project.members.get(id = request.user.id):
            is_member = True
    except:
        is_member = False

    context = {'viewing_project':viewing_project, 'tasks':tasks, 'is_owner':is_owner, 'project_members_not_owner':project_members_not_owner, 'project_members':project_members, 'is_member':is_member, 'all_leaders':all_leaders , 'msgs':msgs}
    ##action when a form is submitted
    if request.method=='POST':
        ##user delete the project
        if request.POST.get('deleteyes'):
            viewing_project.delete()
            time.sleep(3)
            return redirect('/index/')
        ##user close this project
        elif request.POST.get('closeyes'):
            viewing_project.closed = True
            viewing_project.save()
        ##user add new members into the project
        elif request.POST.get('add_name'):
            target_user_name = request.POST.get('add_name')
            if User.objects.get(username=target_user_name):
                target_user = User.objects.get(username=target_user_name)
                viewing_project.members.add(target_user)
        ##remove a member
        elif request.POST.get('remove_name'):
            target_user_id = request.POST.get('remove_name')
            target_user = viewing_project.members.get(id=target_user_id)
            viewing_project.members.remove(target_user)
            try:
                if viewing_project.owner.get(id=target_user_id):
                    viewing_project.owner.remove(target_user)
            except:
                pass
        elif request.POST.get('add_owner'):
            target_user_id = request.POST.get('add_owner')
            target_user = User.objects.get(id=target_user_id)
            viewing_project.owner.add(target_user)
        elif request.POST.get('change_project_name'):
            viewing_project.project_name = request.POST.get('change_project_name')
            viewing_project.save()
        elif request.POST.get('change_project_description'):
            viewing_project.project_description = request.POST.get('change_project_description')
            viewing_project.save()
        elif request.POST.get('make_public'):
            viewing_project.private = False
            viewing_project.save()
        elif request.POST.get('make_private'):
            viewing_project.private = True
            viewing_project.save()
        elif request.POST.get('chat_text'):
            newchatmessage = Chat()
            newchatmessage.belong_project = viewing_project
            newchatmessage.chat_content = request.POST.get('chat_text')
            newchatmessage.speaker = request.user
            newchatmessage.sent_date = datetime.now()
            newchatmessage.save()

    return render(request, 'project.html', context)

def view_task(request, id1 , id2):
    ## view the detail page of a task
    task = Tasks.objects.get(id = id2)
    viewing_project = Project.objects.get(id=id1)
    taskfiles = File.objects.filter(belong_task = id2)
    project_members = viewing_project.members.all()
    project_members_in_charge = task.incharge.all()
    project_members_not_in_charge = viewing_project.members.exclude(id__in = project_members_in_charge)
    uploadfile = File()
    try:
        if task.incharge.get(id = request.user.id):
            is_incharge = True
    except:
        is_incharge = False
    try:
        if viewing_project.members.get(id = request.user.id):
            is_member = True
    except:
        is_member = False
    context = {'viewing_project':viewing_project, 'task':task, 'taskfiles':taskfiles, 'is_incharge':is_incharge, 'project_members_not_in_charge':project_members_not_in_charge, 'is_member':is_member, 'project_members_in_charge':project_members_in_charge}
    if request.method =='POST':
        ##user add new incharge person from members of the project of the task
        if request.POST.get('add_incharge'):
            add_incharge_id = request.POST.get('add_incharge')
            add_incharge_user = User.objects.get(id = add_incharge_id)
            task.incharge.add(add_incharge_user)
        ##user upload files for this task
        elif request.POST.get('myfile_flag'):
            if request.FILES['myfile']:
                uploadfile.belong_task = Tasks.objects.get(id = id2)
                uploadfile.file = request.FILES['myfile']
                uploadfile.filename = request.FILES['myfile'].name
                uploadfile.last_modify = datetime.now()
                uploadfile.save()
        elif request.POST.get('finished'):
            task.finish = True
            task.save()
        elif request.POST.get('unfinished'):
            task.finish = False
            task.save()
        elif request.POST.get('change_task_name'):
            task.task_name = request.POST.get('change_task_name')
            task.save()
        elif request.POST.get('change_task_description'):
            task.task_description = request.POST.get('change_task_description')
            task.save()
        elif request.POST.get('delete_file'):
            target_file_id = request.POST.get('delete_file')
            target_file = File.objects.get(id = target_file_id)
            target_file.delete()
    return render(request, 'task.html', context)

def download(request, id):
    target_file = File.objects.get(id = id)
    target_file_name = target_file.filename
    target_file_name = target_file_name.replace(" ","_")
    file_type = target_file_name.split(".")
    target_file_path = os.path.join(settings.MEDIA_ROOT, target_file_name)
    fp = open(target_file_path ,'rb')
    response = StreamingHttpResponse(fp)
    response['Content-Type'] =  'image/png'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(target_file_name))
    return response
    
def join_project(request, id):
    pj = Project.objects.get(id=id)
    join_request = JoinMessage()
    if request.method == "POST":
        if request.POST.get('va_password') != request.user.password:
            print("wrong pw")
        else:
            join_request.pj = pj
            join_request.user = request.user
            join_request.message = request.POST.get('message')
            join_request.save()
    context = {"pj": pj}
    return render(request, 'join_project.html', context)
 #   join = Project.objects.get(id=id)
  #  return render(request, 'join_project.html')

def join_btn(request):
    return render(request, 'join_project.html')
