# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'orientation', 'uploaded_by', 'uploaded_at')

admin.site.register(models.Photo, PhotoAdmin)
