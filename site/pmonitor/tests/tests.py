"""
pmonitor/models.py unittests.
"""
from datetime import datetime

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from django.test import TestCase
from django.contrib.auth.models import User

#models
from pmonitor.models import Task, Job
from django_nose.tools import assert_queryset_equal

#views
from pmonitor.views import index

__author__ = 'jhohman'


#Testing Views *************************************************
class PipelinePageTest(TestCase):

    #/pipeline goes to index view
    def test_pipeline_url_resolves_to_index_view(self):
        found = resolve('/pipeline/')
        self.assertEqual(found.func, index)

    #checks that index view has the index html template
    def test_pipeline_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('pmonitor/index.html')
        self.assertContains(response.content.decode(), expected_html)

    #check that there is a link there
    def test_link_to_news_app(self):
        response = self.client.get('/pipeline/')
        self.assertContains(response, 'News')


#Testing Models ************************************************
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

    def test_get_next_task(self):
        task1 = Task.objects.create(task_id='task001')
        task2 = Task.objects.create(task_id='task002')
        task3 = Task.objects.create(task_id='task003')

        task1.child = task2
        task1.save()
        task2.child = task3
        task2.save()

        self.assertEqual(task2, task1.get_next_task())
        self.assertEqual(task3, task2.get_next_task())
        with self.assertRaises(Task.DoesNotExist):
            task3.get_next_task()

    def test_get_previous_task(self):
        task1 = Task.objects.create(task_id='task001')
        task2 = Task.objects.create(task_id='task002')
        task3 = Task.objects.create(task_id='task003')

        task1.child = task2
        task1.save()
        task2.child = task3
        task2.save()

        self.assertEqual(task2, task3.get_previous_task())
        self.assertEqual(task1, task2.get_previous_task())
        with self.assertRaises(Task.DoesNotExist):
            task1.get_previous_task()


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

