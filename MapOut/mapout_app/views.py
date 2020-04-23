from django.http import HttpResponseRedirect, FileResponse, StreamingHttpResponse,JsonResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.core import serializers
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from MapOut.settings import EMAIL_HOST_USER
from .forms import *
from .models import *
import time
import os
import json


#this add capital
def create_budget(request, id1):
    viewing_project = Project.objects.get(id = id1)
    viewing_plan = Budgetplan.objects.get(belong_project = viewing_project)
    context = {'viewing_project':viewing_project, 'viewing_plan':viewing_plan}
    if request.method == 'POST':
        if (request.POST.get('capital_name') != '') and (request.POST.get('capital_amount') != ''):
                transition_capital =                        Budget()
                transition_capital.transition_category =    "budget"
                transition_capital.transition_type =        request.POST.get('capital_transition_type')
                transition_capital.belong_plan =            Budgetplan.objects.get(id = id1)
                transition_capital.name =                   request.POST.get('capital_name')
                transition_capital.description =            request.POST.get('capital_description')
                transition_capital.amount =                 int(request.POST.get('capital_amount'))
                transition_capital.save()
    return render(request, 'budget/create_plan.html', context)

##this is add expense
def create_budget_2(request, id1):
    viewing_project = Project.objects.get(id = id1)
    viewing_plan = Budgetplan.objects.get(belong_project = viewing_project)
    context = {'viewing_project':viewing_project, 'viewing_plan':viewing_plan}
    if request.method == 'POST':
        if request.POST.get('expense_name'):
                transition_expense =                        Budget()
                transition_expense.transition_category =    "expense"
                transition_expense.transition_type =        request.POST.get('expense_transition_type')
                transition_expense.belong_plan =            Budgetplan.objects.get(id = id1)
                transition_expense.name =                   request.POST.get('expense_name')
                transition_expense.description =            request.POST.get('expense_description')
                transition_expense.amount =                 int(request.POST.get('expense_amount'))
                transition_expense.save()
    return render(request, 'budget/create_plan_2.html', context)

def view_budget(request, id3): # id3 is project id \
    total_budget  = 0
    total_expense = 0
    total_budget_capital = 0
    total_budget_subsidize = 0
    total_budget_other = 0
    total_expense_manpower = 0
    total_expense_equipment = 0
    total_expense_transport = 0
    total_expense_administrative_fee = 0
    total_expense_consultant_fee = 0
    total_expense_professional_service = 0
    total_expense_miscellaneous = 0
    total_expense_other = 0
    budget_capital_percent = 0      
    budget_subsidize_percent = 0    
    budget_other_percent = 0        
    expense_manpower_percent = 0    
    expense_equipment_percent = 0   
    expense_transport_percent = 0   
    expense_administrative_fee_percent = 0  
    expense_consultant_fee_percent = 0      
    expense_professional_service_percent = 0 
    expense_miscellaneous_percent = 0
    expense_other_percent = 0       
    net = 0
    net_percent = 0
    viewing_project = Project.objects.get(id = id3)
    viewing_plan = Budgetplan.objects.get(belong_project = viewing_project)
    all_budget = Budget.objects.filter(belong_plan = viewing_plan)
    try:
        if viewing_project.members.get(id = request.user.id):
            is_member = True
    except:
        is_member = False
    ##filter out all capital/expense
    budget  = all_budget.filter(transition_category = 'budget')
    expense = all_budget.filter(transition_category = 'expense')
    budget_capital =                all_budget.filter(transition_type = 'Capital')
    budget_subsidize =              all_budget.filter(transition_type = 'Subsidize')
    budget_other =                  all_budget.filter(transition_type = 'Other', transition_category = 'capital')
    expense_manpower =              all_budget.filter(transition_type = 'Manpower')
    expense_equipment =             all_budget.filter(transition_type = 'Equipment')
    expense_transport =             all_budget.filter(transition_type = 'Transport')
    expense_administrative_fee =    all_budget.filter(transition_type = 'Administrative_Fee')
    expense_consultant_fee =        all_budget.filter(transition_type = 'Consultant_Fee')
    expense_professional_service =  all_budget.filter(transition_type = 'Professional_Service')
    expense_miscellaneous =         all_budget.filter(transition_type = 'Miscellaneous')
    expense_other =                 all_budget.filter(transition_type = 'Other', transition_category = 'expense')
    for i in budget:
        total_budget += i.amount
    for i in expense:
        total_expense += i.amount
    for i in budget_capital:
        total_budget_capital += i.amount
    for i in budget_subsidize:
        total_budget_subsidize += i.amount
    for i in budget_other:
        total_budget_other += i.amount
    for i in expense_manpower:
        total_expense_manpower += i.amount
    for i in expense_equipment:
        total_expense_equipment += i.amount
    for i in expense_transport:
        total_expense_transport += i.amount
    for i in expense_administrative_fee:
        total_expense_administrative_fee += i.amount
    for i in expense_consultant_fee:
        total_expense_consultant_fee += i.amount
    for i in expense_professional_service:
        total_expense_professional_service += i.amount
    for i in expense_miscellaneous:
        total_expense_miscellaneous += i.amount
    for i in expense_other:
        total_expense_other += i.amount
    if total_budget != 0:
        budget_capital_percent      = total_budget_capital  /total_budget*100
        budget_subsidize_percent    = total_budget_subsidize/total_budget*100
        budget_other_percent        = total_budget_other    /total_budget*100 
    if total_expense != 0:      
        expense_manpower_percent    = total_expense_manpower    /total_expense*100         
        expense_equipment_percent   = total_expense_equipment   /total_expense*100        
        expense_transport_percent   = total_expense_transport   /total_expense*100        
        expense_administrative_fee_percent      = total_expense_administrative_fee  /total_expense*100
        expense_consultant_fee_percent          = total_expense_consultant_fee      /total_expense*100  
        expense_professional_service_percent    = total_expense_professional_service/total_expense*100
        expense_miscellaneous_percent   = total_expense_miscellaneous   /total_expense*100
        expense_other_percent           = total_expense_other           /total_expense*100 
    net = total_budget-total_expense
    if total_budget != 0:
        net_percent = net/total_budget*100
    arg = ""
    if net_percent>0:
        if net_percent>50:
            arg = "You have more than half of budget remaining."
        else:
            if net_percent>20:
                arg = "You have less than half of budget remaining."
            else:
                arg = "You have little budget remaining. Please be careful of consumption."
    else:
        if net_percent>-50:
            arg = "You are over budget. Please be careful of consumption."
        else:
            arg = "You are seriously over budget. Please be careful of consumption. Please work with a better budget management next time."
    context = {
        "total_budget": total_budget,
        "total_expense": total_expense,
        "total_budget_capital": total_budget_capital,
        "total_budget_subsidize": total_budget_subsidize,
        "total_budget_other": total_budget_other,
        "total_expense_manpower": total_expense_manpower,
        "total_expense_equipment": total_expense_equipment,
        "total_expense_transport": total_expense_transport,
        "total_expense_administrative_fee": total_expense_administrative_fee,
        "total_expense_consultant_fee": total_expense_consultant_fee,
        "total_expense_professional_service": total_expense_professional_service,
        "total_expense_miscellaneous": total_expense_miscellaneous,
        "total_expense_other": total_expense_other,
        "budget_capital_percent"   : budget_capital_percent,
        "budget_subsidize_percent" : budget_subsidize_percent,
        "budget_other_percent"     : budget_other_percent,
        "expense_manpower_percent" : expense_manpower_percent,
        "expense_equipment_percent": expense_equipment_percent,
        "expense_transport_percent": expense_transport_percent,
        "expense_administrative_fee_percent"   : expense_administrative_fee_percent,
        "expense_consultant_fee_percent"       : expense_consultant_fee_percent,
        "expense_professional_service_percent" : expense_professional_service_percent,
        "expense_miscellaneous_percent": expense_miscellaneous_percent,
        "expense_other_percent"        : expense_other_percent,
        "net": net,
        "net_percent": net_percent,
        "arg": arg,
        "viewing_project": viewing_project,
        "is_member": is_member
    }
        #return render(request, 'budget/view_plan.html', context)
    return render(request, 'budget/view_plan.html',context)

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
    request_list=[]
    for i in JoinMessage.objects.filter(user_id = request.user.id, not_reply=True):#filting the project id that have message sent by current user.
        request_list.append(Project.objects.get(id=i.pj_id))
    tasks = Tasks.objects.filter(belong_project__in = projects)  ##filter all the task in the list of project objects
    if request.method == 'POST':
        join_request = JoinMessage()
        join_request.pj = Project.objects.get(id=request.POST.get('JPID'))
        join_request.user = request.user
        join_request.message = request.POST.get('message')
        join_request.save()
        return HttpResponseRedirect(request.path)
    context = {
        'projects':projects, 
        'tasks':tasks, 
        'all_public_project': all_public_project, 
        'cuser':request.user,
        'request_list': request_list
        }
    return render(request, 'main_projects.html', context)


def index_tasks(request):
    tasks = Tasks.objects.filter(incharge = request.user).order_by('finish')
    context = {'tasks':tasks}
    return render(request, 'main_tasks.html', context)

def login_btn(request):
    return render(request, 'registration/login.html') 

###need modify!!
'''
def pw_enter(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            html_msg = render_to_string('registration/reset_email.html', {'content': 'request.user.username'})
            plain_msg = strip_tags(html_msg)
            send_mail('Reset Password', plain_msg,
                'mapoutproject@gmail.com',[email],
                html_message=html_msg)
            return redirect("home.html")
    else:
        return render(request, 'registration/password_reset_form.html')

    #####
    '''

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
            return render(request, 'home.html')

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
            send_mail(
                        'Welcome To MapOut!',
                        'Dear @'+ username + ',\nYou have successfully registered on MapOut. \n\nHave Fun!:)\n\nBest, \nMapOut Team',
                        'mapoutproject@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def schedule(request):
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    user_tasks = Tasks.objects.filter(incharge = request.user).order_by('-due_date')
    today = datetime.now()
    #print((str(today.month))+'haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    this_month = int(str(today.month))
    get_days = days[this_month-1]
    this_month = months[this_month-1]
    #print(str(get_days) + 'YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
    user_tasks = user_tasks.filter(due_date__year = today.year, due_date__month = today.month).order_by('due_date')
    user_tasks_date = user_tasks.all()
    array = []
    for each_date in user_tasks_date:
        array.append(int(each_date.due_date.strftime('%d')))
    print(array)
    js_data = json.dumps(serializers.serialize('json',user_tasks))
    
    context = {'user_tasks':user_tasks, 'today':today, 'this_month':this_month, 'get_days':range(1,get_days+1),'js_data':js_data,'days_of_tasks':array}
    
    return  render(request, 'schedule.html',context)


def help_(request):
    return  render(request, 'help.html')

def settings_(request):
    target = User.objects.get(id=request.user.id)
    target_profile = Profile.objects.get(user_id=target.id)
    pati_project = request.user.members
    own_project = request.user.owner
    ##update here
    if request.method == "POST":
        target.username = request.POST.get('cUsername')
        target.email = request.POST.get('cEmail')
        target.private = request.POST.get('Privacy')
        target.save()
        target_profile.gender = request.POST.get('gender')
        target_profile.date_birth = request.POST.get('birthday')
        target_profile.description = request.POST.get('sdes')
        target_profile.save()
    context={
        'user': target,
        'profile': target_profile,
        'pproject': pati_project,
        'oproject': own_project
    }
    return  render(request, 'settings.html', context)

def create_project(request):
    createproject = Project()
    createbudgetplan = Budgetplan()
    if request.method == 'POST':
        if request.POST.get('project_name') and request.POST.get('project_description'):
            createproject.project_name = request.POST.get('project_name')
            createproject.project_description = request.POST.get('project_description')
            createproject.private = request.POST.get('project_privacy')
            createproject.create_date = datetime.now()
            createproject.save()
            createproject.owner.add(request.user)    ##add current user as owner
            createproject.members.add(request.user)   ##add current user as a member
            createbudgetplan.belong_project = createproject
            createbudgetplan.save()
            #messages.success(request, 'You have successfully created a project.')
            send_mail(
                'Project Created!',
                'Dear @'+ request.user.username + ',\nYou have successfully created project ' + createproject.project_name + 
                ' on MapOut. Have fun!\nBest, \nMapOut Team',
                'mapoutproject@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
            
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
            createtask.start_date = request.POST.get('start_date')
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
    #for join messages handling
    join_requests = JoinMessage.objects.filter(pj_id = viewing_project.id)
    non_r_msg = join_requests.filter(not_reply = True)  ## see if the request user is the owner of the project
    senders = []
    for i in join_requests:
        senders.append(User.objects.get(id = i.user_id))

    all_announcement = Announcement.objects.filter(belong_project = viewing_project).order_by('-pinned')
    reverse_ordered_announcements = Announcement.objects.filter(belong_project = viewing_project).order_by('-id')

    print(all_announcement)
    print(reverse_ordered_announcements)

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
    context = {
        'viewing_project':viewing_project, 
        'tasks':tasks, 'is_owner':is_owner, 
        'project_members_not_owner':project_members_not_owner, 
        'project_members':project_members, 
        'request': request,
        'is_member':is_member, 
        'all_leaders':all_leaders , 
        'msgs':msgs,
        'join_requests':join_requests,
        'non_r_msg': non_r_msg,
        'all_announcement':all_announcement,
        'reverse_ordered_announcements':reverse_ordered_announcements,
        'senders': senders
    }
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
                send_mail(
                    'You are now a memeber of Project' + viewing_project.project_name + '!',
                    'Dear @'+ target_user.username + ',\nYou were added to the project ' + viewing_project.project_name + ' by @' + request.user.username + 
                    ' on MapOut. \n\nYou can now view, edit and monitor your project after login MapOut! If you need help, please check the help center.\n\nHave fun! \n\nBest, \nMapOut Team',
                    'mapoutproject@gmail.com',
                    [target_user.email],
                    fail_silently=False,
                )
                new_user_announce = Announcement()
                new_user_announce.belong_project = viewing_project
                new_user_announce.message = target_user_name + " just join our team!"
                new_user_announce.save()
        ##remove a member
        elif request.POST.get('remove_name'):
            target_user_id = request.POST.get('remove_name')
            target_user = viewing_project.members.get(id=target_user_id)
            viewing_project.members.remove(target_user)
            send_mail(
                        'You were removed from project ' + viewing_project.project_name + '.',
                        'Dear @'+ target_user.username + ',\nYou were removed from the project ' 
                        + viewing_project.project_name + ' by @' + request.user.username + 
                        ' on MapOut. \n\nIf you need help, please check the help center.\n\nHave fun! \n\nBest, \nMapOut Team',
                        'mapoutproject@gmail.com',
                        [target_user.email],
                        fail_silently=False,
            )
            try:
                if viewing_project.owner.get(id=target_user_id):
                    viewing_project.owner.remove(target_user)
            except:
                pass
            new_user_announce = Announcement()
            new_user_announce.belong_project = viewing_project
            new_user_announce.message = target_user.username + " leave our team."
            new_user_announce.save()
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
        elif request.POST.get('accept'):
            target_msg = JoinMessage.objects.get(id=request.POST.get('accept'))
            sender = User.objects.get(id=target_msg.user_id)
            viewing_project.members.add(sender)
            target_msg.not_reply=False
            target_msg.save()
            new_user_announce = Announcement()
            new_user_announce.belong_project = viewing_project
            new_user_announce.message = sender.username + " just join our team!"
            new_user_announce.save()
        elif request.POST.get('reject'):
            target_msg = JoinMessage.objects.get(id=request.POST.get('reject'))
            target_msg.not_reply=False
            target_msg.save()
        elif request.POST.get('new_announcement'):
            new = Announcement()
            new.belong_project = viewing_project
            new.message = request.POST.get('new_announcement')
            if request.POST.get('pin'):
                new.pinned = request.POST.get('pin')
            new.save()

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
    context = {
        'viewing_project':viewing_project, 
        'task':task, 'taskfiles':taskfiles, 
        'is_incharge':is_incharge, 
        'project_members_not_in_charge':project_members_not_in_charge, 
        'is_member':is_member, 
        'project_members_in_charge':project_members_in_charge
        }
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
        elif request.POST.get('download_file'):
            file = File.objects.get(id =request.POST.get('download_file'))
            filename = file.file.name.split('/')[-1]
            response = HttpResponse(file.file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
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
