from django.forms import ModelForm, TextInput, Textarea, DateInput, ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Task
from datetime import date

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'task_status','start_date', 'completed_date']

        widgets = {
            'name': TextInput(attrs={'placeholder':'Task Title', 'class': 'w-full px-4 py-6 mt-4'}),
            'description': Textarea(attrs={'placeholder':'Description of the task', 'class': 'w-full px-4 py-6 mt-4 rounded-xl border'}),
            'due_date': DateInput(attrs={'class': 'w-full px-4 py-6 mt-4', 'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}),
        }

        def clean_date(self):
            d = self.cleaned_data.get('due_date')

            if d < date.today():
                raise ValidationError('Due date cannot be in the past')
            return d

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['title'].widget.attrs['class'] = 'form-control'
            self.fields['description'].widget.attrs['class'] = 'form-control'
            self.fields['task_status'].widget.attrs['class'] = 'form-control'

class ChangeStatusForm(ModelForm):
    class Meta:
        model = Task
        fields = ('task_status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_status'].widget.attrs['class'] = 'form-control'

class AssignUserForm(ModelForm):
    class Meta:
        model = Task
        fields = ('assign_user', )


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    username = forms.CharField(
        widget=forms.TextInput(attrs={
        'Placeholder': 'Your Username',
        'class': 'w-full px-6 py-3 border rounded-xl'
         }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'Placeholder': 'Your First Name',
        'class': 'w-full px-6 py-3 border rounded-xl'
        }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'Placeholder': 'Your last name',
        'class': 'w-full px-6 py-3 border rounded-xl'
        }))


    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email address',
        'class' : 'w-full py-3 px-6 rounded-xl border',
        }))

    password1 = forms.CharField(
        label= 'Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your Password',
            'class' : 'w-full px-6 py-3 rounded-xl border-b',
            }))

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat Password',
            'class': 'w-full px-6 py-3 border rounded-xl'
            }))

class LogInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = forms.CharField(
        widget=forms.TextInput(attrs={
        'Placeholder': 'Your Username',
        'class': 'w-full px-6 py-3 border rounded-xl'
        }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'Placeholder': 'Your Password',
        'class': 'w-full px-6 py-3 border rounded-xl'
        }))


        # widgets = {
        #     'username': TextInput(attrs={'placeholder': 'Enter your username', 'class':'w-full px-4 py-2 border rounded-xl'}),
        #     'email': EmailInput(attrs={'placeholder':'Your Email address', 'class':'w-full px-4 py-2 border rounded-xl'}),
        #     'first_name': TextInput(attrs={'placeholder': 'Your first name', 'class': 'w-full px-4 py-2 border rounded-xl'}),
        #     'last_name': TextInput(attrs={'placeholder': 'Your last name', 'class': 'w-full px-4 py-2 border rounded-xl'}),
        #     'password1': PasswordInput(attrs={'placeholder': 'Password', 'class': 'w-full px-4 py-2 border rounded-xl'}),
        #     'password2': PasswordInput(attrs={'placeholder': 'Repeat password', 'class': 'w-full px-4 py-2 border rounded-xl'}),
        # }
