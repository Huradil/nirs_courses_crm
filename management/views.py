from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib import messages

from account.models import Student
from .forms import CourseForm, MaterialForm, TaskForm, CompletedTaskForm, CompletedTaskFeedbackForm
from .models import Course, Material, Task, CompletedTask
from .mixins import BasePermissionMixin
from .functions import is_user_or_admin


class CourseCreateView(BasePermissionMixin, View):
    template_name = 'management/course_create.html'
    permission_required = ['Teacher', 'Admin']
    sidebar_group = 'Курсы'
    sidebar_name = 'Создать курс'
    sidebar_icon = 'fas fa-plus'

    def get(self, request):
        form = CourseForm()
        return render(request, 'management/course_create.html', {'form': form})

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        print(form.errors)
        return render(request, 'management/course_create.html', {'form': form})

    def handle_permission_denied(self, request, exception):
        return render(request, '403.html')


class CourseListView(View):
    template_name = 'management/course_list.html'

    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'management/course_list.html', {'courses': courses})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'management/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object
        context['materials'] = Material.objects.filter(course=self.object)
        context['tasks'] = Task.objects.filter(course=self.object)
        context['students'] = self.object.students.all()
        context['material_form'] = MaterialForm()
        context['task_form'] = TaskForm()
        context['is_teacher_or_admin'] = is_user_or_admin(self.request.user)
        return context

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        course = self.get_object()
        if not user.is_superuser and user not in [student.user for student in course.students.all()] and not \
                user == course.teacher:
            return render(request, '403.html')
        return super().dispatch(request, *args, **kwargs)


def add_course_material(request, course_pk):
    if request.method == 'POST':
        try:
            course = Course.objects.get(pk=course_pk)
            Material.objects.create(
                course=course,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                file=request.FILES.get('file'),
            )
            messages.success(request, 'Материал успешно добавлен')
            return redirect('course_detail', pk=course_pk)
        except Exception as e:
            messages.error(request, f'Произошла ошибка: {e}')
            return redirect('course_detail', pk=course_pk)


def add_course_task(request, course_pk):
    if request.method == 'POST':
        try:
            course = Course.objects.get(pk=course_pk)
            Task.objects.create(
                course=course,
                title=request.POST.get('title'),
                task=request.POST.get('task'),
                description=request.POST.get('description'),
                file=request.FILES.get('file'),
                date_end=request.POST.get('date_end'),
                max_score=request.POST.get('max_score'),
                material=Material.objects.get(pk=request.POST.get('material')) if request.POST.get(
                    'material') else None,
            )
            return redirect('course_detail', pk=course_pk)
        except Exception as e:
            messages.error(request, f'Произошла ошибка: {e}')
            return redirect('course_detail', pk=course_pk)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'management/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        context['completed_tasks'] = CompletedTask.objects.filter(task=self.object)
        context['completed_task_form'] = CompletedTaskForm()
        context['is_teacher_or_admin'] = is_user_or_admin(self.request.user)
        return context


def send_course_task(request, task_pk):
    if request.method == 'POST':
        try:
            task = Task.objects.get(pk=task_pk)
            student = Student.objects.get(user=request.user)
            CompletedTask.objects.create(
                student=student,
                task=task,
                file=request.FILES.get('file') if request.FILES.get('file') else None,
                text=request.POST.get('text') if request.POST.get('text') else None,
            )
            return redirect('task_detail', pk=task_pk)
        except Exception as e:
            messages.error(request, f'Произошла ошибка: {e}')
            return redirect('task_detail', pk=task_pk)


class CompletedTaskDetailView(BasePermissionMixin, DetailView):
    model = CompletedTask
    template_name = 'management/completed_task_detail.html'
    permission_required = ['Teacher', 'Admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        context['mark_task_form'] = CompletedTaskFeedbackForm()
        context['is_teacher_or_admin'] = is_user_or_admin(self.request.user)
        return context

    def has_perms(self, perm_list, obj=None):
        value = any(self.has_perm(perm, obj) for perm in perm_list)
        if value:
            return value
        return self.request.user == self.get_object().student.user


def mark_course_task(request, pk):
    if request.method == 'POST':
        try:
            completed_task = CompletedTask.objects.get(pk=pk)
            completed_task.score = request.POST.get('score')
            completed_task.feedback = request.POST.get('feedback')
            completed_task.save()
            return redirect('task_detail', pk=completed_task.task.pk)
        except Exception as e:
            messages.error(request, f'Произошла ошибка: {e}')
            return redirect('task_detail', pk=completed_task.task.pk)
