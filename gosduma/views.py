from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse
from django.template.defaulttags import register
from django.shortcuts import render, redirect
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import *


def createlog(r, newlog):
    if Logs.objects.all().count() > 100:
        temp = Logs.objects.order_by('id')[:1]
        temp[0].delete()
    if Logs.objects.all():
        last = Logs.objects.order_by('-id')[:1]
        if newlog != last[0].log or r.user.username != last[0].author:
            if r.user.is_authenticated:
                Logs(author=f'{r.user.username}', log=newlog).save()
            else:
                Logs(author=f'Анонимный пользователь', log=newlog).save()
    else:
        Logs(author=f'System', log='Initial log').save()


@login_required
def show_logs(request):
    return render(request, 'Showlogs.html', {'header': 'Логи', 'logs': Logs.objects.all()})


@register.filter
def normalfile(value):
    name = ''
    flag = False
    for i in range(len(value)):
        if flag:
            name += value[i]
        if value[i] == '/':
            flag = True
    return name


@register.filter
def getmb(value):
    return round(((value / 1024) / 1024), 2)


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
    createlog(request, 'Посетил главную страницу')
    if request.user.is_authenticated:
        a = request.user.social_auth.all()
        for i in a:
            if i.provider == 'facebook':
                name = i.extra_data['name']
                user = User.objects.get(username=request.user)
                user.username = name + str(f" (Facebook)")
                user.save()
            elif i.provider == 'google-oauth2':
                user = User.objects.get(username=request.user)
                user.username = request.user.first_name + str(f" (Google+)")
                user.save()
            elif i.provider == 'vk-oauth2':
                user = User.objects.get(username=request.user)
                user.username = request.user.first_name + ' ' + request.user.last_name + str(f" (VK)")
                user.save()
    allposts = Posts.objects.all()
    allnames = Posts.objects.all()[:5]
    return render(request, 'index.html',
                  {'header': 'Сайт депутата мосгордумы Василия Пупкина', 'posts': allposts, 'allnames': allnames})


def about_us(request):
    createlog(request, 'Посетил страницу \'О нас\'')
    return render(request, 'about.html', {'header': 'О нас'})


@login_required
def add_post(request):
    createlog(request, 'Посетил страницу \'Добавить новость\'')
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            createlog(request, f'Создал новость')
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
        createlog(request, 'Посетил страницу \'Добавить запрос\'')
        form = AddRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            createlog(request, f'Создал обращение')
            return redirect('index')
    else:
        form = AddRequestForm(initial={
            'author': request.user.username,
            'recipient': 1,
            'email':request.user.email,
            'FIO': f'{request.user.first_name} {request.user.last_name}'
        })
    context = {
        'form': form,
        'header': 'Добавить запрос'
    }
    return render(request, 'add_post.html', context=context)


def showpost(request, post_id):
    post = Posts.objects.get(pk=post_id)
    createlog(request, f'Посмотрел пост \' {post.name} \'')
    return render(request, 'showpost.html', {'post': post})


@login_required
def show_requests(request, typee):
    svalue = 'None'
    if typee == 'my':
        createlog(request, 'Посетил страницу \'Мои запросы\'')
        all_requests = Request.objects.filter(author=request.user)
        superus = 1
    else:
        createlog(request, 'Посетил страницу \'Все запросы\'')
        query = request.GET.get('s')
        svalue = query
        if query:
            all_requests = Request.objects.filter(Q(subject__contains=query) | Q(tag__name__contains=query))
        else:
            all_requests = Request.objects.all()
        superus = 0
    return render(request, 'showrequests.html',
                  {'searchval': svalue, 'header': 'Обращения', 'requests': all_requests, 'super': superus})


@login_required
def show_request(request, req_id):
    req = Request.objects.get(pk=req_id)
    createlog(request, f'Посмотрел запрос \'{req.subject}\'')
    return render(request, 'show_request.html', {'request': req})


@login_required
def answer(request, req_pk):
    createlog(request, f'Посетил страницу \' Ответ на запрос \'')
    answeron = Request.objects.get(pk=req_pk)
    if request.method == 'POST':
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            form.save()
            createlog(request, f'Ответил на запрос \'{answeron.subject}\'')
            return redirect('all_request', 'all')
    else:
        form = AddAnswerForm(initial={'author': request.user.username, 'answeron': answeron})
    context = {
        'answeron': answeron,
        'form': form,
        'header': 'Ответить',
        'type': 'answer'
    }
    return render(request, 'add_post.html', context=context)


@login_required
def my_answers(request):
    createlog(request, f'Посетил страницу \' Мои ответы \'')
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
    createlog(request, f'Вышел')
    logout(request)
    return redirect('index')
