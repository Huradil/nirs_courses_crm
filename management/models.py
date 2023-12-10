from django.db import models

from account.models import Student, Teacher


class Course(models.Model):
    course_name = models.CharField(verbose_name='Наименование курса', max_length=150)
    students = models.ManyToManyField(Student, verbose_name='Студенты')
    teacher = models.ForeignKey(Teacher, verbose_name='Преподаватель', on_delete=models.PROTECT)
    materials = models.ManyToManyField('Material', verbose_name='Материалы курса')


def upload_materials(instance, file_name):
    return f'course_materials/{instance} - {file_name}'


class Material(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=150)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    file = models.FileField(verbose_name='Файл', upload_to=upload_materials, null=True, blank=True)


class Tasks(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=150)
    task = models.TextField(verbose_name='Задание')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    file = models.FileField(verbose_name='Файл', upload_to=upload_materials, null=True, blank=True)




