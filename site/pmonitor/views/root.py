import logging
from django.shortcuts import render

log = logging.getLogger(__name__)

__author__ = 'jhohman'


def root(request):
    log.info('root view')
    template = 'pmonitor/base.html'
    return render(request, template)
