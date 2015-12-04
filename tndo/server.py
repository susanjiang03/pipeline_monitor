import tornado.ioloop
import tornado.web
from tornado import websocket

GLOBALS = dict(
    sockets=[]
)
LOG_FILE = '/tmp/pipeline.log'


def get_line_from_file():
    filename = LOG_FILE
    print 'get_line_from_file %s' % filename

    with open(filename, 'r') as the_file:
        for line in the_file:
            parsed = line.strip()

            if not parsed:
                continue
            yield parsed


CAT = get_line_from_file()


def iter_line():
    try:
        line = CAT.next()
    except StopIteration:
        pass
    else:
        print 'Iter...'
        for socket in GLOBALS['sockets']:
            socket.write_message(line)


class ClientSocket(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        GLOBALS['sockets'].append(self)
        print "WebSocket opened"

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
    periodic = tornado.ioloop.PeriodicCallback(iter_line, 5000, io_loop=main)
    periodic.start()
    main.start()
