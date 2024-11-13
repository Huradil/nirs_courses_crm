from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import render
from management.mixins import BasePermissionMixin
from management.models import Course

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


class StudentListView(BasePermissionMixin, View):
    permission_required = ["Teacher", "Admin"]
    sidebar_group = 'Студенты'
    sidebar_name = 'Список студентов'
    sidebar_icon = 'fas fa-list'

    def get(self, request):
        students = Student.objects.all()
        students_data = []
        for student in students:
            students_data.append({
                'id': student.id,
                'fio': student.full_name,
                'courses': ', '.join([course.course_name for course in Course.objects.filter(students=student)]),
                "email": student.user.email,
            })
        return render(request, 'account/student_list.html', {'students': students_data})

