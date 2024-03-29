# Generated by Django 4.0.4 on 2022-05-13 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gosduma', '0010_alter_tags_options_request_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='file',
            field=models.FileField(null=True, upload_to='files/', verbose_name='Приложение'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gosduma.statuses', verbose_name='Статус'),
        ),
    ]
