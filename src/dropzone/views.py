# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.views.generic.simple import direct_to_template

from . import JsonResponse
from . forms import PhotoForm


@login_required
def index(request):
    context = {}
    return direct_to_template(request, 'dropzone/index.html', context)


@login_required
def upload(request):
    status = 400
    response = None
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.name = obj.resource.name
        obj.save(request.user)
        status = 200
        response = {'success': 200}
    else:
        response = {'error': 400}
        response.update({'errors': form.errors})
    return JsonResponse(response, status=status)
