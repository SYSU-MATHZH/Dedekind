from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from sua.models import Sua, Sua_Application, Proof, Student


class LoginForm(forms.Form):
    user_name = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'text_box'})
    )
    user_password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'text_box'})
    )
    loginstatus = forms.BooleanField(required=False)


class SuaForm(ModelForm):
    class Meta:
        model = Sua
        fields = [
            'group',
            'title',
            'team',
            'date',
            'suahours',
        ]
        widgets = {
            'group': forms.Select(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入活动名称',
            }),
            'team': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'date': AdminDateWidget(attrs={
                'class': 'form-control',
            }),
            'suahours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入公益时数',
            }),

        }


class ProofForm(ModelForm):
    class Meta:
        model = Proof
        fields = [
            'is_offline',
            'proof_file',
        ]
        widgets = {
        }


class Sua_ApplicationForm(ModelForm):
    class Meta:
        model = Sua_Application
        fields = [
            'detail',
            'contact',
        ]
        widgets = {
            'detail': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入活动详情',
                'cols': 20,
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入联系方式',
            })
        }
