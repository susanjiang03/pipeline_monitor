import logging
from django.shortcuts import render
from django.contrib import messages
from random import randint

log = logging.getLogger(__name__)

__author__ = 'jhohman'


def index(request):
    log.info('index view')
    template = 'pmonitor/index.html'
    messages.info(request, "I'm a server generated random int! %d" % randint(1, 100))
    messages.warning(request, "Try to dismiss this warning!")
    return render(request, template)
