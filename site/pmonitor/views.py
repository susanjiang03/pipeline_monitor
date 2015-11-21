import logging
from django.shortcuts import render

__author__ = 'jhohman'
log = logging.getLogger(__name__)


def index(request):
    log.info('index view')
    template = 'pmonitor/index.html'
    return render(request, template)

