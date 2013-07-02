# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.views.generic.simple import direct_to_template


@login_required
def index(request):
    context = {}
    return direct_to_template(request, 'frontend/login.html', context)
