from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView, View
from django.urls import reverse, reverse_lazy


from .forms import UserForm


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    sidebar_group = 'Пользователи'
    sidebar_name = 'Создать пользователя'
    sidebar_icon = 'fas fa-user-plus'
    success_message = 'Вы успешно зарегестрировались'
