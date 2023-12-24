from django.urls import path

from . import views

urlpatterns = [
    path('course/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:course_pk>/material/add/', views.add_course_material, name='add_course_material'),
    path('course/<int:course_pk>/task/add/', views.add_course_task, name='add_course_task'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:task_pk>/send/', views.send_course_task, name='send_task'),
    path('completed_task/<int:pk>/', views.CompletedTaskDetailView.as_view(), name='completed_task_detail'),
    path('completed_task/<int:pk>/mark/', views.mark_course_task, name='mark_task'),
]
