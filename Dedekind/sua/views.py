from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import LoginForm


@login_required
def index(request):
    usr = request.user
    sua_list = []
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
        i = 0
        for sua in stu.sua_set.order_by('-date'):
            i += 1
            sua_list.append((i, sua))
    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
        suahours = '-.-'
    return render(request, 'sua/index.html', {
        'stu_name': name,
        'stu_number': number,
        'stu_suahours': suahours,
        'sua_list': sua_list,
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['user_password']
            loginstatus = form.cleaned_data['loginstatus']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if(loginstatus):
                    request.session.set_expiry(15*24*3600)
                else:
                    request.session.set_expiry(0)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login')
    else:
        form = LoginForm()
    return render(request, 'sua/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required
def apply_sua(request):
    usr = request.user
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
    else:
        if usr.is_staff:
            name = 'Admin.' + usr.username
        else:
            name = 'NoStuInfo.' + usr.username
        number = '------'
    date = timezone.now()
    year = date.year
    month = date.month
    if month < 9:
        year_before = year - 1
        year_after = year
    else:
        year_before = year
        year_after = year + 1

    return render(request, 'sua/apply_sua.html', {
        'stu_name': name,
        'stu_number': number,
        'apply_date': date.date(),
        'apply_year_before': year_before,
        'apply_year_after': year_after,
    })
