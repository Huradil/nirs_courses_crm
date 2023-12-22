# Generated by Django 4.1.3 on 2023-12-21 20:08

from django.db import migrations, models
import management.models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_course_period_alter_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedtask',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=management.models.upload_task, verbose_name='Файл'),
        ),
        migrations.AddField(
            model_name='completedtask',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Ответ'),
        ),
    ]
