from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from PIL import Image


class Role(models.Model):
    name = models.CharField(max_length=150, verbose_name='Роль пользователя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


def user_directory_path(instance, filename):
    return f'images/avatar/account/{instance.id}/{filename}'


class User(AbstractUser):
    roles = models.ManyToManyField(Role, verbose_name='Роли пользователя')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество')
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path, verbose_name='Аватарка')
    fullname = models.CharField(max_length=150, verbose_name='ФИО', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='account', blank=True)
    user_groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='account', blank=True)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Логин')
    full_name = models.CharField(verbose_name='ФИО Преподавателя', max_length=150)
    name = models.CharField(verbose_name='Имя', max_length=150)

    def __str__(self):
        return self.full_name








class SidebarGroup(models.Model):
    """
    Модель, представляющая группу элементов бокового меню.
    """
    name: models.CharField = models.CharField(max_length=255, verbose_name='Название')
    icon = models.CharField(max_length=255, verbose_name='Иконка')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in User.objects.all():
            key = make_template_fragment_key('sidebar', [user.username])
            cache.delete(key)

    class Meta:
        verbose_name = 'Группа бокового меню'
        verbose_name_plural = 'Группы бокового меню'


class AvailableURLs(models.Model):
    """
    Модель, представляющая доступные урлы
    """
    function_name = models.CharField(max_length=255, verbose_name='Название')
    url_name = models.CharField(max_length=255, verbose_name='URL')

    def __str__(self):
        return f'{self.function_name} {self.url_name}'

    class Meta:
        verbose_name = 'Доступный URL'
        verbose_name_plural = 'Доступные URL'


class SidebarItem(models.Model):
    """
    Модель, представляющая элемент бокового меню.

        Атрибуты:
    - display_name: отображаемое название элемента.
    - url: связанный доступный URL.
    - icon: иконка элемента.
    - group: связанная группа элементов.
    """
    display_name = models.CharField(max_length=255, verbose_name='Название')
    url = models.ForeignKey(AvailableURLs, on_delete=models.CASCADE, verbose_name='URL', null=True, blank=True)
    icon = models.CharField(max_length=255, verbose_name='Иконка')
    group = models.ForeignKey(SidebarGroup, on_delete=models.CASCADE, verbose_name='Группа', related_name='items')

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = 'Элемент бокового меню'
        verbose_name_plural = 'Элементы бокового меню'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in User.objects.all():
            key = make_template_fragment_key('sidebar', [user.username])
            cache.delete(key)


class SidebarItemChild(models.Model):
    """
        Модель для дочерних элементов бокового меню.

    Атрибуты:
    - display_name: отображаемое название дочернего элемента.
    - url: связанный доступный URL.
    - icon: иконка дочернего элемента.
    - parent_item: связанный родительский элемент.
    """
    display_name = models.CharField(max_length=255, verbose_name='Название')
    url = models.ForeignKey(AvailableURLs, on_delete=models.CASCADE, verbose_name='URL')
    icon = models.CharField(max_length=255, verbose_name='Иконка')
    parent_item = models.ForeignKey(SidebarItem, on_delete=models.CASCADE, verbose_name='Подгруппа',
                                    related_name='children')

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = 'Элемент бокового подменю'
        verbose_name_plural = 'Элементы бокового подменю'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in User.objects.all():
            key = make_template_fragment_key('sidebar', [user.username])
            cache.delete(key)




