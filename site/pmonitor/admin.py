from django.contrib import admin
from pmonitor.models import Job, Task

__author__ = 'jhohman'


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created_date')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_id', 'task_name', 'task_description')

admin.site.register(Job, JobAdmin)
admin.site.register(Task, TaskAdmin)

