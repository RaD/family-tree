# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'src.frontend.views',
    url(r'^$', 'index', name='index'),
)
