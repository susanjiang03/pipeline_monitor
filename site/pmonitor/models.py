from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

__author__ = 'jhohman'

class Task(models.Model):
    parent = models.ForeignKey("self", related_name='task_parents', null=True, blank=True)
    child = models.ForeignKey("self", related_name='task_children', null=True, blank=True)
    siblings = models.ForeignKey("self", related_name='task_siblings', null=True, blank=True)
    task_id = models.CharField(blank=True, max_length=64)
    task_name = models.CharField(blank=True, max_length=256)
    task_description = models.CharField(blank=True, max_length=1024)


class Job(models.Model):
    """
    A job (a pipeline) is a parent object that holds a series of tasks.
    """
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(default=datetime.now)
    entry_task = models.ForeignKey(Task, null=True, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    name = models.CharField(max_length=256, blank=True)

