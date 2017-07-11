from django import forms


class LoginForm(forms.Form):
    user_name = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'text_box'}))
    user_password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'text_box'}))
    loginstatus = forms.BooleanField(required=False)
