import logging
from django.shortcuts import render
from django.core.urlresolvers import reverse

__author__ = 'jhohman'
log = logging.getLogger(__name__)


def index(request):
    log.info('index view')
    template = 'pmonitor/index.html'
    extra_context = dict(
        site_title='Pipeline Monitor',
        right_menu=dict(
            menu_title='Jobs',
            menu_items=[
                dict(
                    label='Run Populate Articles Job',
                    url='javascript:void(0);',
                    onclick='javascript:populate_articles();'
                )
            ]
        ),
        main_nav=[
            dict(
                label='Pipeline', url=reverse('pmonitor:index'), active=True
            ),
            dict(
                label='News', url=reverse('news:index'),
                active=False
            ),
            dict(
                label='Admin Site', url=reverse('admin:index'), active=False
            ),
        ]
    )
    return render(request, template, extra_context)
