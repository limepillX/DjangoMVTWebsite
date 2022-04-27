from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.template.defaulttags import register
from django.shortcuts import render, redirect
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import *


@register.filter
def getamountmessages(user):
    print(user)
    a = RequestAnswer.objects.filter(answeron__author=user)
    print(a)
    b = 0
    for i in a:
        b += 1
    return b


@register.filter
def get_date(value):
    now = datetime.now()
    return now.date()


@register.filter
def get_time(value):
    now = datetime.now()
    return now.time()


def index(request):
    if request.user.is_authenticated:
        a = request.user.social_auth.all()
        for i in a:
            if i.provider == 'facebook':
                name = i.extra_data['name']
                user = User.objects.get(username=request.user)
                user.username = name + str(f" (Facebook)")
                user.save()
            elif i.provider == 'instagram':
                name = i.extra_data['user']['full_name']
                print(name)
                user = User.objects.get(username=request.user)
                user.username = name + str(f" (Instagram)")
                user.save()
            elif i.provider == 'google-oauth2':
                user = User.objects.get(username=request.user)
                user.username = request.user.first_name + str(f" (Google+)")
                user.save()
    allposts = Posts.objects.all()
    allnames = Posts.objects.all()[:5]
    return render(request, 'index.html', {'header': 'Главная', 'posts': allposts, 'allnames': allnames})


def about_us(request):
    return render(request, 'about.html', {'header': 'О нас'})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddPostForm(initial={'author': request.user.username})
    context = {
        'form': form,
        'header': 'Добавить новость'
    }
    return render(request, 'add_post.html', context=context)


@login_required
def add_request(request):
    if request.method == 'POST':
        form = AddRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddRequestForm(initial={'author': request.user.username, 'recipient': 1})
    context = {
        'form': form,
        'header': 'Добавить запрос'
    }
    return render(request, 'add_post.html', context=context)


def showpost(request, post_id):
    post = Posts.objects.get(pk=post_id)
    return render(request, 'showpost.html', {'post': post})


@login_required
def show_requests(request, typee):
    if typee == 'my':
        all_requests = Request.objects.filter(author=request.user)
        superus = 1
    else:
        all_requests = Request.objects.all()
        superus = 0
    return render(request, 'showrequests.html', {'header': 'Обращения', 'requests': all_requests, 'super': superus})


@login_required
def show_request(request, req_id):
    req = Request.objects.get(pk=req_id)
    return render(request, 'show_request.html', {'request': req})


@login_required
def answer(request, req_pk):
    if request.method == 'POST':
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_request', 'all')
    else:
        form = AddAnswerForm(initial={'author': request.user.username, 'answeron': Request.objects.get(pk=req_pk)})
    context = {
        'form': form,
        'header': 'Ответить'
    }
    return render(request, 'add_post.html', context=context)


@login_required
def my_answers(request):
    req = RequestAnswer.objects.filter(answeron__author=request.user.username)
    return render(request, 'showrequests.html', {'header': 'Мои ответы', 'requests': req, 'super': 1})


class RequestUpdateView(UpdateView):  # Новый класс
    form_class = ChangeStatusForm
    model = Request
    template_name = 'edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = Request
        return context


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('index')


def mustbelogined(request):
    return render(request, 'showtext.html', {'text': 'Вы должны войти, чтобы сделать это действие!'})


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')
