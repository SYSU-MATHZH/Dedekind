from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import LoginForm, SuaForm, Sua_ApplicationForm, ProofForm
from .models import Proof


@login_required
def index(request):
    usr = request.user
    sua_list = []
    sa_list = []
    if hasattr(usr, 'student'):
        stu = usr.student
        name = stu.name
        number = stu.number
        suahours = stu.suahours
        i = 0
        for sua in stu.sua_set.filter(is_valid=True).order_by('-date'):
            i += 1
            sua_list.append((i, sua))
        i = 0
        for sua in stu.sua_set.order_by('-sua_application__date'):
            if hasattr(sua, 'sua_application'):
                i += 1
                sa_list.append((i, sua.sua_application))
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
        'sa_list': sa_list,
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
                    request.session.set_expiry(15 * 24 * 3600)
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
    stu = None
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

    # 表单处理
    if request.method == 'POST':
        suaForm = SuaForm(request.POST, prefix='suaForm')
        proofForm = ProofForm(request.POST, request.FILES, prefix='proofForm')
        sua_ApplicationForm = Sua_ApplicationForm(
            request.POST,
            prefix='sua_ApplicationForm',
        )
        if suaForm.is_valid() and\
                proofForm.is_valid() and\
                sua_ApplicationForm.is_valid() and\
                stu is not None:
            # 生成Models
            if proofForm.cleaned_data['is_offline']:
                offlineProofSet = Proof.objects.filter(is_offline=True)
                if offlineProofSet.count == 0:
                    assert(User.objects.filter(is_superuser=True).count != 0)
                    proof = Proof.objects.create(
                        user=User.objects.filter(is_superuser=True)[0],
                        date=date,
                        is_offline=True,
                    )
                    proof.save()
                else:
                    proof = offlineProofSet[0]
            else:
                proof = proofForm.save(commit=False)
            sua = suaForm.save(commit=False)
            sua_Application = sua_ApplicationForm.save(commit=False)
            # 处理proof
            if not proofForm.cleaned_data['is_offline']:
                proof.user = usr
                proof.date = date
                proof.save()
            # 处理sua
            sua.student = stu
            sua.last_time_suahours = 0.0
            sua.is_valid = False
            sua.save()
            # 处理sua_Application
            sua_Application.sua = sua
            sua_Application.date = date
            sua_Application.proof = proof
            sua_Application.is_checked = False
            sua_Application.save()
            return HttpResponseRedirect('/')
    else:
        suaForm = SuaForm(prefix='suaForm')
        proofForm = ProofForm(prefix='proofForm')
        sua_ApplicationForm = Sua_ApplicationForm(
            prefix='sua_ApplicationForm',
        )

    return render(request, 'sua/apply_sua.html', {
        'stu_name': name,
        'stu_number': number,
        'apply_date': date.date(),
        'apply_year_before': year_before,
        'apply_year_after': year_after,
        'proofForm': proofForm,
        'suaForm': suaForm,
        'sua_ApplicationForm': sua_ApplicationForm,
    })
