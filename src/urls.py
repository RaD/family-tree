# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^accounts/login/$', login, {'template_name': 'frontend/login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dropzone/', include('src.dropzone.urls', namespace='dropzone')),
    url(r'^galleria/', include('src.galleria.urls', namespace='galleria')),
    url(r'^', include('src.frontend.urls', namespace='frontend')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, }), )
