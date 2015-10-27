from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

__author__ = 'jhohman'

# ToDo: Models...
# class Task(models.Model):
#     parent = models.ForeignKey("self")
#     child = models.ForeignKey("self")
#     siblings = models.ForeignKey("self")
#
#
# class Pipeline(models.Model):
#     """
#     A pipeline is a parent object that holds a series of tasks.
#     """
#     user = models.ForeignKey(User)
#     date = models.DateTimeField(default=datetime.now())
#     tasks = models.ManyToManyField(Task)
