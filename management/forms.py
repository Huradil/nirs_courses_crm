from django import forms

from .models import Course, Material, Task, CompletedTask
from .mixins import FormControlMixin


class CourseForm(FormControlMixin, forms.ModelForm):
    date_start = forms.DateField(
        label='Дата начала курса',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = Course
        fields = ['course_name', 'students', 'teacher', 'date_start', 'date_end', 'period', 'description']


class MaterialForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Material
        fields = ['file', 'title', 'description', ]


class TaskForm(FormControlMixin, forms.ModelForm):
    date_end = forms.DateField(
        label='Дата окончания',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    material = forms.ModelChoiceField(
        label='Материал',
        queryset=Material.objects.all(),
        required=False,
    )

    class Meta:
        model = Task
        fields = ['file', 'title', 'task', 'description', 'date_end', 'max_score', 'material']


class CompletedTaskForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = CompletedTask
        fields = ['file', 'text']


class CompletedTaskFeedbackForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = CompletedTask
        fields = ['score', 'feedback']
