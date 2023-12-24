from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from PIL import Image


class Role(models.Model):
    name = models.CharField(max_length=150, verbose_name='Роль пользователя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


def user_directory_path(instance, filename):
    return f'images/avatar/users/{instance.id}/{filename}'


class User(AbstractUser):
    roles = models.ManyToManyField(Role, verbose_name='Роли пользователя')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество')
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path, verbose_name='Аватарка')
    fullname = models.CharField(max_length=150, verbose_name='ФИО', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)
    user_groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='users', blank=True)
    user_set = None

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        if not self.fullname:
            self.fullname = f'{self.last_name} {self.first_name}'
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    def has_permission_user(self, perm: str, obj=None) -> bool:
        # Если у пользователя есть права администратора, то он имеет доступ ко всему
        if self.is_superuser:
            return True

        user_role = self.roles.all()
        # Проверяем есть ли в группах пользователя права на выполнение действия
        if user_role.filter(name=perm).exists():
            return True
        return False

    def get_fullname(self):
        return self.fullname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Логин')
    full_name = models.CharField(verbose_name='ФИО студента', max_length=150)
    name = models.CharField(verbose_name='Имя', max_length=150)

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Преподаватель')
    full_name = models.CharField(verbose_name='ФИО студента', max_length=150)
    name = models.CharField(verbose_name='Имя', max_length=150)

    def __str__(self):
        return self.full_name




