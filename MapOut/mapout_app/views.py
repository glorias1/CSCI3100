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
from django.contrib.auth.hashers import check_password
from MapOut.settings import EMAIL_HOST_USER
from .forms import *
from .models import *
import time
import os


def index_budgets(request):
    if request.method == 'POST':
        if request.POST.get('createplan'):
            return render(request, 'budget/create_plan.html')
    return render(request, 'budget/index.html')

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
                transition_capital.belong_project =         Project.objects.get(id = id1)
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
                transition_expense.belong_project =         Project.objects.get(id = id1)
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
    viewing_project = Project.objects.get(id = id3)
    viewing_plan = Budgetplan.objects.get(belong_project = viewing_project)
    all_budget_records = Budget.objects.filter(belong_plan = viewing_plan)
    try:
        if viewing_project.members.get(id = request.user.id):
            is_member = True
    except:
        is_member = False
    ##filter out all capital/expense
    all_budget = Budget.objects.filter(belong_plan = viewing_plan)
    budget  = all_budget.filter(transition_category = 'capital')
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
    budget_capital_percent      = total_budget_capital  /total_budget*100
    budget_subsidize_percent    = total_budget_subsidize/total_budget*100
    budget_other_percent        = total_budget_other    /total_budget*100       
    expense_manpower_percent    = total_expense_manpower    /total_expense*100         
    expense_equipment_percent   = total_expense_equipment   /total_expense*100        
    expense_transport_percent   = total_expense_transport   /total_expense*100        
    expense_administrative_fee_percent      = total_expense_administrative_fee  /total_expense*100
    expense_consultant_fee_percent          = total_expense_consultant_fee      /total_expense*100  
    expense_professional_service_percent    = total_expense_professional_service/total_expense*100
    expense_miscellaneous_percent   = total_expense_miscellaneous   /total_expense*100
    expense_other_percent           = total_expense_other           /total_expense*100 
    net = total_budget-total_expense
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
        "net_percent": net/total_budget*100,
        "arg": arg
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
    tasks = Tasks.objects.filter(belong_project__in = projects)  ##filter all the task in the list of project objects
    context = {'projects':projects, 'tasks':tasks, 'all_public_project': all_public_project, 'cuser':request.user}
    return render(request, 'main_projects.html', context)

def index_tasks(request):
    tasks = Tasks.objects.filter(incharge = request.user).order_by('finish')
    context = {'tasks':tasks}
    return render(request, 'main_tasks.html', context)

def login_btn(request):
    return render(request, 'registration/login.html') 

def pw_enter(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            html_msg = render_to_string('reset_email.html', {'content': 'request.user.username'})
            plain_msg = strip_tags(html_msg)
            send_mail('Reset Password', plain_msg,
                'mapoutproject@gmail.com',[email],
                html_message=html_msg)
            messages.info(request, 'Email sent!')
            return redirect("home")
    else:
        return render(request, 'registration/password_reset_form.html')

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
            send_mail(
                        'Welcome To MapOut!',
                        'Dear @'+ username + '\nYou have successfully registered on MapOut. Have Fun!:)\n Best, \nMapOut Team',
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
    return  render(request, 'schedule.html')

def help_(request):
    return  render(request, 'help.html')

def settings_(request):
    return  render(request, 'settings.html')

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
            messages.success(request, 'You have successfully created a project.')
            send_mail(
                'Welcome To MapOut!',
                'Dear @'+ request.user.username + '\nYou have successfully created project' + createproject.project_name + 
                'on MapOut. Have fun!\n Best, \nMapOut Team',
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
    join_requests = JoinMessage.objects.filter(pj_id = viewing_project.id)
    non_r_msg = join_requests.filter(not_reply = True)
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
    context = {
        'viewing_project':viewing_project, 
        'tasks':tasks, 'is_owner':is_owner, 
        'project_members_not_owner':project_members_not_owner, 
        'project_members':project_members, 
        'is_member':is_member, 
        'all_leaders':all_leaders , 
        'msgs':msgs,
        'join_requests':join_requests,
        'non_r_msg': non_r_msg
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
        elif request.POST.get('accept'):
            target_msg = JoinMessage.objects.get(id=request.POST.get('accept'))
            sender = User.objects.get(id=target_msg.user_id)
            viewing_project.members.add(sender)
            target_msg.not_reply=False
            target_msg.save()
        elif request.POST.get('reject'):
            target_msg = JoinMessage.objects.get(id=request.POST.get('reject'))
            target_msg.not_reply=False
            target_msg.save()

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
    
def join_project(request, pid):
    pj = Project.objects.get(id=pid)
    join_request = JoinMessage()
    ##should not allow dup. messages.
    if request.method == "POST":
        #print("typein pas: " + request.POST.get('va_password'))
        #print("user's pw: " + request.user.password)
        if check_password(request.POST.get('va_password'), request.user.password):
            join_request.pj = pj
            join_request.user = request.user
            join_request.message = request.POST.get('message')
            join_request.save()
        else:
            pass#print("wrong password")
        #context={"join_request": join_request, "pj": pj}
    return HttpResponseRedirect("/projects/")#render(request, 'main_projects.html')
