from django.db import models
from django.urls import reverse

from account.models import Student, Teacher


class Course(models.Model):
    course_name = models.CharField(verbose_name='Наименование курса', max_length=150)
    students = models.ManyToManyField(Student, verbose_name='Студенты')
    teacher = models.ForeignKey(Teacher, verbose_name='Преподаватель', on_delete=models.PROTECT)
    date_start = models.DateField(verbose_name='Дата начала курса')
    date_end = models.DateField(verbose_name='Дата окончания курса', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    period = models.DecimalField(verbose_name='Длительность курса', null=True, blank=True, max_digits=5,
                                 decimal_places=2)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})

        # Метод добавляющий кнопку редактирования

    def get_button(self):
        return f"""
               <a href="{self.get_absolute_url()}">
                 <i class="bi bi-search"></i> 
               </a>
           """

    def __str__(self):
        return self.course_name


def upload_materials(instance, file_name):
    return f'course_materials/{instance} - {file_name}'


class Material(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Наименование', max_length=150)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    file = models.FileField(verbose_name='Файл', upload_to=upload_materials, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title


class Task(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, verbose_name='Материал', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Наименование', max_length=150)
    task = models.TextField(verbose_name='Задание')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    file = models.FileField(verbose_name='Файл', upload_to=upload_materials, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date_end = models.DateTimeField(verbose_name='Дата окончания', null=True, blank=True)
    max_score = models.DecimalField(verbose_name='Максимальный балл', max_digits=5, decimal_places=2, null=True,
                                    blank=True)

    def __str__(self):
        return self.title


def upload_task(instance, file_name):
    return f'task/{instance} - {file_name}'


class CompletedTask(models.Model):
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.PROTECT)
    task = models.ForeignKey(Task, verbose_name='Задание', on_delete=models.PROTECT)
    file = models.FileField(verbose_name='Файл', upload_to=upload_task, null=True, blank=True)
    text = models.TextField(verbose_name='Ответ', null=True, blank=True)
    score = models.DecimalField(verbose_name='Балл', max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(verbose_name='Дата выполнения', auto_now_add=True)
    feedback = models.TextField(verbose_name='Отзыв', null=True, blank=True)

    def __str__(self):
        return self.task.title




