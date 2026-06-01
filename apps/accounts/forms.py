from django import forms
from django.contrib.auth.models import User


# Cadastro de novo usuario (a senha e tratada com set_password na view).
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        widgets = {'password': forms.PasswordInput()}


# Alteracao de dados do usuario (sem mexer em senha/username).
class UserChangeInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
