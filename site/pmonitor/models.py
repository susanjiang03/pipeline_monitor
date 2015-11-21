"""
Pipeline models.
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

__author__ = 'jhohman'


class Task(models.Model):
    """
    Task model.
    """
    parent = models.ForeignKey(
        "self", related_name='parent_of', null=True, blank=True
    )
    child = models.ForeignKey(
        "self", related_name='child_of', null=True, blank=True
    )
    siblings = models.ManyToManyField("self", blank=True)
    task_id = models.CharField(blank=True, max_length=64)
    task_name = models.CharField(blank=True, max_length=256)
    task_description = models.CharField(blank=True, max_length=1024)

    def __str__(self):
        return '<Task %s>' % self.task_id

    def save(self, update=True, *args, **kwargs):
        """
        Subclassed save method to propagate Task relationships.

        :param update: flag to prevent infinite recursion on propagation.
        :type update: bool.
        :returns: None.
        """
        super(Task, self).save(*args, **kwargs)
        if update:
            if self.parent:
                self.parent.child = self
                self.parent.save(update=False)
            if self.child:
                self.child.parent = self
                self.child.save(update=False)


class Job(models.Model):
    """
    A job (a pipeline) is a parent object that holds a series of tasks.
    """
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(default=datetime.now)
    entry_task = models.ForeignKey(Task, null=True, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return '<Job %s, user: %s>' % (self.name, self.user.get_username())

