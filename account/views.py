from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView


from .forms import UserForm, LoginUserForm
from .models import Student, Teacher, Role


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')
    sidebar_group = 'Пользователи'
    sidebar_name = 'Создать пользователя'
    sidebar_icon = 'fas fa-user-plus'
    success_message = 'Вы успешно зарегестрировались'

    def form_valid(self, form):
        response = super().form_valid(form)
        if get_object_or_404(Role, name='Student') in self.object.roles.all():
            Student.objects.create(
                user=self.object,
                full_name=self.object.fullname,
                name=self.object.first_name
            )
        if get_object_or_404(Role, name='Teacher') in self.object.roles.all():
            Teacher.objects.create(
                user=self.object,
                full_name=self.object.fullname,
                name=self.object.first_name
            )
        return response


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'
