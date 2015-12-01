import logging
from django.shortcuts import render

__author__ = 'jhohman'
log = logging.getLogger(__name__)


def index(request):
    log.info('index view')
    template = 'pmonitor/index.html'
    extra_context = dict(
        site_title='Pipeline Monitor',
        # right_menu=dict(
        #     menu_title='Menu',
        #     menu_items=[
        #         dict(label='Admin Site', url='admin/')
        #     ]
        # ),
        main_nav=[
            dict(label='Admin Site', url='admin/', active=False),
            # dict(label='Nav2', url='#', active=False),
        ]
    )
    return render(request, template, extra_context)

