from django.contrib import admin

from .models import User, Role


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('fullname',)
    list_filter = ('fullname', )
    list_per_page = 10


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = ('name', )
    list_per_page = 10
