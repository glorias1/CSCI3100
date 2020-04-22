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
from django.core.mail import send_mail
from .forms import *
from .models import *
from .settings import EMAIL_HOST_USER
import time
import os

def index_budgets(request):
    if request.method == 'POST':
        if request.POST.get('createplan'):
            return render(request, 'budget/create_plan.html')
    return render(request, 'budget/index.html')

def create_budget(request):
    projects = Project.objects.filter(id = 1)
    options = {'projects':projects}
    if request.method == 'POST':
        if request.POST.get('belong_project_select'):
            selected_project_id = request.POST.get('belong_project_select')
    
            if (request.POST.get('capital_name') != '') and (request.POST.get('capital_amount') != ''):
                transition_capital =            Budget()
                transition_capital.transition_type = "capital"
                transition_capital.belong_project = Project.objects.get(id = selected_project_id)
                transition_capital.name =       request.POST.get('capital_name')
                transition_capital.amount =     int(request.POST.get('capital_amount'))
                transition_capital.save()
    
            if (request.POST.get('expense_1_name') != '') and (request.POST.get('expense_1_amount') != ''):
                transition_expense_1 =          Budget()
                transition_expense_1.transition_type = "expense"
                transition_expense_1.belong_project = Project.objects.get(id = selected_project_id)
                transition_expense_1.name =     request.POST.get('expense_1_name')
                transition_expense_1.amount =   int(request.POST.get('expense_1_amount'))
                transition_expense_1.save()
 
            if (request.POST.get('expense_2_name') != '') and (request.POST.get('expense_2_amount') != ''):       
                transition_expense_2 =          Budget()
                transition_expense_2.transition_type = "expense"
                transition_expense_2.belong_project = Project.objects.get(id = selected_project_id)
                transition_expense_2.name =     request.POST.get('expense_2_name')
                transition_expense_2.amount =   int(request.POST.get('expense_2_amount'))
                transition_expense_2.save()
    
            if (request.POST.get('expense_3_name') != '') and (request.POST.get('expense_3_amount') != ''):     
                transition_expense_3 =          Budget()
                transition_expense_3.transition_type = "expense"
                transition_expense_3.belong_project = Project.objects.get(id = selected_project_id)
                transition_expense_3.name =     request.POST.get('expense_3_name')
                transition_expense_3.amount =   int(request.POST.get('expense_3_amount'))
                transition_expense_3.save()

    return render(request, 'budget/create_plan.html')

def create_budget_2(request):
    if request.method == 'POST':
        if request.POST.get('expense_name'):
            transition_expense =          Budget()
            transition_expense.transition_type = "expense"
            transition_expense.belong_project = Project.objects.get(id = 1) # selected_project_id)
            transition_expense.name =     request.POST.get('expense_name')
            transition_expense.amount =   int(request.POST.get('expense_amount'))
            transition_expense.save()
    return render(request, 'budget/create_plan_2.html')

def view_budget(request, id3): # id3 is project id 
    if request.method == 'GET':
        total_expense = 0
        capital = Budget.objects.raw('SELECT * FROM mapout_app_budget WHERE belong_project_id = %s AND transition_type = "capital"', [id3])
        expense = Budget.objects.raw('SELECT * FROM mapout_app_budget WHERE belong_project_id = %s AND transition_type = "expense"', [id3])
        for i in expense:
            total_expense += i.amount
        context = {
            "capital": capital[0].amount,
            "expense": total_expense
        }
        return render(request, 'budget/view_plan.html', context)
    return render(request, 'budget/view_plan.html', context)

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
    context = {'projects':projects, 'tasks':tasks, 'all_public_project': all_public_project, 'cuser':request.user}
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
            user.profile.
            private = form.cleaned_data.get('privacy')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            send_mail(
                        'Welcome To MapOut!',
                        'Dear '+ username + '\nYou have successfully registered on MapOut. Have Fun!:)\n Best, \nMapOut Team',
                        'mapoutproject',
                        [user.email],
                        fail_silently=False,
                    )
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
