# -*- coding: utf-8 -*-

from dateutil import parser

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from . import get_exif


def upload_photos_dir(instance, filename):
    u"""Возвращает путь для загружаемого файла, учитывая данные exif."""
    exif = get_exif(instance.resource.file)
    ts = exif.get('DateTimeOriginal')
    if ts:
        ts = parser.parse(ts)
        return u'dropzone/photos/%s/%s/%s/%s' % (ts.year, ts.month, ts.day, filename)
    else:
        return u'dropzone/photos/no-exif/%s' % (filename)


class Photo(models.Model):
    EXIF_NOPE = 1
    EXIF_HF = 2
    EXIF_UD = 3
    EXIF_VF = 4
    EXIF_VFR = 5
    EXIF_R = 6
    EXIF_HFR = 7
    EXIF_L = 8
    EXIF_ORIENTATION_CHOICES = (
        (EXIF_NOPE, _('No action')),
        (EXIF_HF, _('Horizontal flip')),
        (EXIF_UD, _('Left 180 degrees')),
        (EXIF_VF, _('Vertical flip')),
        (EXIF_VFR, _('Vertical flip and right 90 degrees')),
        (EXIF_R, _('Right 90 degrees')),
        (EXIF_HFR, _('Horizontal flip and right 90 degrees')),
        (EXIF_L, _('Left 90 degrees')), )

    resource = models.FileField(upload_to=upload_photos_dir, max_length=256, verbose_name=_('Resource'))
    file_name = models.CharField(max_length=256, verbose_name=_('Name'))
    file_type = models.CharField(max_length=80, verbose_name=_('MIME'))
    file_size = models.PositiveIntegerField(default=0, verbose_name=_('Size'))
    orientation = models.PositiveIntegerField(default=1, verbose_name=_('Orientation'), choices=EXIF_ORIENTATION_CHOICES)
    uploaded_by = models.ForeignKey('auth.User', related_name=u'uploaded_by', verbose_name=_('Uploader'))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-uploaded_at', )
        verbose_name = _(u'Resource')
        verbose_name_plural = _(u'Resources')
        ordering = ('-uploaded_at', )

    def __unicode__(self):
        return self.file_name

    def save(self, user):
        f = self.resource.file
        self.uploaded_by = user
        self.file_name = f.name
        self.file_type = f.content_type
        self.file_size = f.size
        exif = get_exif(self.resource.file)
        self.orientation = exif.get('Orientation', 1)
        super(Photo, self).save()
