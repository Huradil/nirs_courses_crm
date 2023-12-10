from django import forms

from .models import Course
from .mixins import FormControlMixin


class CourseForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


