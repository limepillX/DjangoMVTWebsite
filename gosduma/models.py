from django.conf import settings
from django.db import models
from django.urls import reverse


class Request(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.ForeignKey('Statuses', on_delete=models.PROTECT, verbose_name='Статус', default=2)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')
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

