# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.views.generic.simple import direct_to_template

from src.dropzone.models import Photo


@login_required
def index(request):
    context = {
        'object_list': Photo.objects.all(),
    }
    return direct_to_template(request, 'galleria/index.html', context)
