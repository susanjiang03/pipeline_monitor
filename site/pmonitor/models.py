"""
Pipeline models.
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import (
    MaxValueValidator, MinValueValidator, URLValidator
)

__author__ = 'jhohman'


class Status(object):
    """
    Class that acts as an API for various status mappings.
    """
    VALID_STATUS = tuple(range(5))

    SUCCESS = 0
    IN_PROGRESS = 1
    NOT_RUN = 2
    WARNING = 3
    ERROR = 4

    CHOICES = (
        (SUCCESS, 'success'),
        (IN_PROGRESS, 'in progress'),
        (NOT_RUN, 'not run'),
        (WARNING, 'warning'),
        (ERROR, 'error')
    )


class Task(models.Model):
    """
    Task model.
    updated_date is automatically set to datetime.now() on save.
    """
    parent = models.ForeignKey(
        "self", related_name='parent_of', null=True, blank=True
    )
    child = models.ForeignKey(
        "self", related_name='child_of', null=True, blank=True
    )
    siblings = models.ManyToManyField("self", blank=True)
    task_id = models.CharField(blank=True, max_length=64)
    name = models.CharField(blank=True, max_length=256)
    description = models.CharField(blank=True, max_length=1024)
    status = models.PositiveSmallIntegerField(
        default=Status.NOT_RUN,
        validators=[
            MinValueValidator(Status.VALID_STATUS[0]),
            MaxValueValidator(Status.VALID_STATUS[-1])
        ],
        choices=Status.CHOICES
    )
    message = models.CharField(blank=True, max_length=1024)
    url = models.URLField(blank=True, validators=[URLValidator])
    last_run = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.task_id

    def save(self, update=True, *args, **kwargs):
        """
        Subclassed save method to propagate Task relationships.

        :param update: flag to prevent infinite recursion on propagation.
        :type update: bool
        :returns: None
        """
        if self.status == Status.NOT_RUN:
            self.last_run = None
        else:
            self.last_run = datetime.now()
        super(Task, self).save(*args, **kwargs)
        if update:
            if self.parent:
                self.parent.child = self
                self.parent.save(update=False)
            if self.child:
                self.child.parent = self
                self.child.save(update=False)

    def get_previous_task(self):
        """
        Method to traverse the task hierarchy.
        Gets parent task.

        :returns: Task
        :type return: Task
        :raises: DoesNotExist
        """
        if self.parent:
            return self.parent
        raise self.DoesNotExist()

    def get_next_task(self):
        """
        Method to traverse the task hierarchy.
        Gets child task.

        :returns: Task
        :type return: Task
        :raises: DoesNotExist
        """
        if self.child:
            return self.child
        raise self.DoesNotExist()


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
        return '%s, user: %s' % (self.name, self.user.get_username())

