# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson as json

from PIL import Image
from PIL.ExifTags import TAGS
from StringIO import StringIO


class JsonResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        HttpResponse.__init__(self, content=json.dumps(data), mimetype='application/json', **kwargs)



def get_exif(obj):
    ret = {}
    obj.seek(0)
    f = StringIO(obj.read())
    i = Image.open(f)
    info = i._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    return ret
