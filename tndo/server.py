import os
import sys

sys.path.insert(0, '../site')
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "core.settings"
)

import django

django.setup()

import tornado.ioloop
import tornado.web
from tornado import websocket
from pmonitor.models import Task, Status
from json import dumps
from datetime import datetime, date

__author__ = 'jhohman'

GLOBALS = dict(
    sockets=[]
)


class Pipeline(object):
    LINK_WIDTH = 40
    GROUP = 1

    def __init__(self):
        self.status = dict(
            nodes=[],
            links=[]
        )
        self.num_tasks = 0

    def add_task(self, task):
        self.status['nodes'].append(dict(
            group=self.GROUP,
            name=task.name,
            description=task.description,
            status=Status.TRANS[task.status],
            message=task.message,
            url=task.url,
            last_run=task.last_run
        ))

        self.num_tasks += 1
        if self.num_tasks > 1:
            self.status['links'].append(dict(
                source=self.num_tasks - 2,
                target=self.num_tasks - 1,
                value=self.LINK_WIDTH
            ))

    def json_response(self):
        dt_handler = (
            lambda obj: obj.strftime('%m/%d/%Y %I:%M:%S %P')
            if isinstance(obj, datetime) else None
        )
        return dumps(self.status, default=dt_handler)


CACHED_PIPELINE = Pipeline()


def get_task_status():
    task = Task.objects.filter(parent=None)[0]
    yield task
    while True:
        try:
            task = task.get_next_task()
        except Task.DoesNotExist:
            raise StopIteration()
        else:
            yield task


def build_pipeline():
    pipeline = Pipeline()
    for task in get_task_status():
        pipeline.add_task(task)

    return pipeline


def iter_line():
    global CACHED_PIPELINE
    pipeline = build_pipeline()

    json_status = pipeline.json_response()
    old_json_status = CACHED_PIPELINE.json_response()

    if json_status != old_json_status:
        CACHED_PIPELINE = pipeline
        print '\n' + json_status + '\n'
        for socket in GLOBALS['sockets']:
            socket.write_message(json_status)


class ClientSocket(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        GLOBALS['sockets'].append(self)
        print "WebSocket opened"
        pipeline = build_pipeline()
        json_status = pipeline.json_response()
        print "push pipeline"
        self.write_message(json_status)

    def on_close(self):
        print "WebSocket closed"
        GLOBALS['sockets'].remove(self)


class Announcer(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        data = self.get_argument('data')
        for socket in GLOBALS['sockets']:
            socket.write_message(data)

        print 'Posted data: %s' % data
        self.write('Posted data: %s' % data)


application = tornado.web.Application([
    (r"/socket", ClientSocket),
    (r"/push", Announcer),
])

if __name__ == "__main__":
    application.listen(8081)
    main = tornado.ioloop.IOLoop.instance()
    periodic = tornado.ioloop.PeriodicCallback(iter_line, 2000, io_loop=main)
    periodic.start()
    main.start()
