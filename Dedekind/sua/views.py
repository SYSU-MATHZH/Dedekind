from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


@login_required
def index(request):
    usr = request.user
    stu = usr.student
    return render(request, 'sua/index.html', {'stu_name': stu.name, 'stu_number': stu.number, 'stu_suahours': stu.suahours})


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
    return render(request, 'sua/apply_sua.html')
