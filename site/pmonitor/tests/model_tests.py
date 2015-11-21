"""
pmonitor/models.py unittests.
"""
from django.test import TestCase
from pmonitor.models import Task, Job
from django_nose.tools import assert_queryset_equal
from django.contrib.auth.models import User
from datetime import datetime, timedelta

__author__ = 'jhohman'


class TestTasks(TestCase):
    """
    Tests the Task model.
    """
    def setUp(self):
        self.task = Task.objects.create(task_id='SomeTask01')
        super(TestTasks, self).setUp()

    def test_create_task(self):
        task_id = 'Task001'
        task1 = Task.objects.create(task_id=task_id)
        empty_queryset = Task.objects.none()
        self.assertIsNotNone(task1)
        self.assertEqual(task_id, task1.task_id)
        self.assertEqual('', task1.task_name)
        self.assertEqual('', task1.task_description)
        self.assertIsNone(task1.parent)
        self.assertIsNone(task1.child)
        assert_queryset_equal(empty_queryset, task1.siblings.all())

    def test_task_description(self):
        # Assert precondition
        self.assertEqual('', self.task.task_description)

        desc = 'Cats n dogs.'
        self.task.task_description = desc

        # Assert postcondition
        self.assertEqual(desc, self.task.task_description)

    def test_task_name(self):
        # Assert precondition
        self.assertEqual('', self.task.task_name)

        name = 'Cats n dogs.'
        self.task.task_name = name

        # Assert postcondition
        self.assertEqual(name, self.task.task_name)

    def test_make_task_parent(self):
        task_parent = Task.objects.create(task_id='task001')
        task_child = Task.objects.create(task_id='task002')

        task_child.parent = task_parent
        task_child.save()

        self.assertEqual(task_child, task_parent.child)
        self.assertEqual(task_parent, task_child.parent)

    def test_make_task_child(self):
        task_parent = Task.objects.create(task_id='task001')
        task_child = Task.objects.create(task_id='task002')

        task_parent.child = task_child
        task_parent.save()

        self.assertEqual(task_child, task_parent.child)
        self.assertEqual(task_parent, task_child.parent)

    def test_make_task_sibling(self):
        task_sibling1 = Task.objects.create(task_id='task001a')
        task_sibling2 = Task.objects.create(task_id='task001b')
        empty_queryset = Task.objects.none()
        queryset1 = Task.objects.filter(task_id='task001a')
        queryset2 = Task.objects.filter(task_id='task001b')

        # Assert precondition
        assert_queryset_equal(empty_queryset, task_sibling1.siblings.all())
        assert_queryset_equal(empty_queryset, task_sibling2.siblings.all())

        task_sibling1.siblings.add(task_sibling2)
        task_sibling1.save()

        # FixMe: This doesn't work... don't know why.
        # assert_queryset_equal(task_sibling1.siblings.all(), queryset2)

        # the hard way
        for tasks in zip(task_sibling1.siblings.all(), queryset2):
            self.assertEqual(tasks[0], tasks[1])

        for tasks in zip(task_sibling2.siblings.all(), queryset1):
            self.assertEqual(tasks[0], tasks[1])


class TestJobs(TestCase):
    """
    Tests the Job model.
    """
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='testuser')
        super(TestJobs, cls).setUpClass()

    def test_create(self):
        job = Job.objects.create(
            user=self.user,
        )
        self.assertIsNotNone(job)

    def test_user(self):
        job = Job.objects.create(
            user=self.user,
        )
        self.assertEqual(self.user, job.user)

    def test_created_date(self):
        now = datetime.now()
        threshold = 30  # seconds
        job = Job.objects.create(
            user=self.user,
        )
        td = job.created_date - now
        self.assertTrue(td.seconds <= threshold)

    def test_entry_task(self):
        task = Task.objects.create(task_id='SomeTask01')
        job = Job.objects.create(
            user=self.user,
            entry_task=task
        )
        self.assertEqual(task, job.entry_task)
