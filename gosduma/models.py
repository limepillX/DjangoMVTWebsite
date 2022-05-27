from django.conf import settings
from django.db import models
from django.urls import reverse


class Tags(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тэг сообщения')

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Request(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    email = models.EmailField(null=True, verbose_name='Почта для связи')
    FIO = models.CharField(max_length=255, verbose_name='ФИО')
    description = models.TextField(blank=True, verbose_name='Описание')
    file = models.FileField(upload_to ='files/', null=True, verbose_name='Приложение', blank=True)
    status = models.ForeignKey('Statuses', on_delete=models.PROTECT, verbose_name='Статус', null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')
    tag = models.ForeignKey('Tags', on_delete=models.CASCADE, verbose_name='Тэг', default=1)
    author = models.CharField(max_length=255)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Получатель')

    def get_absolute_url(self):
        return reverse('show_request', kwargs={'req_id': self.pk})

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'обращение'
        verbose_name_plural = 'обращения'
        ordering = ['-id']


class RequestAnswer(models.Model):
    answeron = models.ForeignKey('Request', on_delete=models.PROTECT, verbose_name='Запрос')
    description = models.TextField(blank=True, verbose_name='Ответ')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    author = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'
        ordering = ['-id']


class Posts(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    Photo = models.ImageField(upload_to="photos/posts/", verbose_name='Фото', null=True, blank=True,
                              default="notfoundwidth.png")
    Video = models.CharField(max_length=1000, blank=True, verbose_name='Видео (не обязательно)')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')
    author = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('posts', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-id']


class Statuses(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'
        ordering = ['-id']


class Logs(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    author = models.CharField(max_length=255, verbose_name='Кто')
    log = models.CharField(max_length=255, verbose_name='Что сделал')

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
        ordering = ['-id']
