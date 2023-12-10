from django.views import View
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CourseForm
from .models import Course


class CourseCreateView(View):
    template_name = 'management/course_create.html'

    def get(self, request):
        form = CourseForm()
        return render(request, 'account/login.html', {'form': form})

