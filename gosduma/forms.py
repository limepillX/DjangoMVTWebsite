from django import forms
from .models import *


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['name', 'Photo', 'Video', 'description', 'author']
        widgets = {
            'name': forms.TextInput(attrs={'style': "font-size: 25px; width: 450px", 'class': "form-control"}),
            'description': forms.Textarea(attrs={'cols': 100, 'class': "form-control"}),
            'Video': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status']


class AddAnswerForm(forms.ModelForm):
    class Meta:
        model = RequestAnswer
        fields = ['answeron', 'description', 'author']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 100, 'class': "form-control"}),
        }


class AddRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['subject','FIO', 'email', 'description', 'recipient', 'author', 'tag', 'file']
        widgets = {
            'subject': forms.TextInput(attrs={'style': "font-size: 20px; width: 450px", 'class': "form-control"}),
            'FIO': forms.TextInput(attrs={'style': "font-size: 20px; width: 450px", 'class': "form-control"}),
            'email': forms.TextInput(attrs={'style': "font-size: 15px; width: 450px", 'class': "form-control"}),
            'description': forms.Textarea(attrs={'cols': 100, 'class': "form-control"}),
        }
