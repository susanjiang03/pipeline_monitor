import logging
from django.shortcuts import render

log = logging.getLogger(__name__)

__author__ = 'jhohman'


def index(request):
    log.info('index view')
    template = 'pmonitor/index.html'
    print 'root'
    print template
    return render(request, template)
