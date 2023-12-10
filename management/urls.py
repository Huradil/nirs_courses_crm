from django.urls import path

from . import views

urlpatterns = [
    path('course/create/', views.CourseCreateView.as_view(), name='course_create'),
]
