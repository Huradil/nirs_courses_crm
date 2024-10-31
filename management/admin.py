from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ('course_name', )
    list_filter = ('course_name', )
    list_per_page = 10
