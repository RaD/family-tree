# -*- coding: utf-8 -*-

import hashlib
from os.path import join

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager

from src.relatives.models import Person


class Profile(User):
    u"""
    Модель пользователя, наследуемая от User. Предназначена для
    хранения дополнительной информации.
    """

    person = models.OneToOneField(Person)
    photo = models.ImageField(
        _('Photo'), upload_to=join('profile', 'photo'), max_length=255, blank=True, null=True,
        help_text=_(
            'Upload your photo here or we try to get it from <a href="//gravatar.com/">Gravatar</a>.'
            '<br/>We prefer 400x400 size for a photo.'))
    phone = models.CharField(verbose_name=_(u'Phone'), max_length=16,blank=True, null=True)
    address = models.CharField(_('Address'), max_length=255, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profile')
        ordering = ('last_name', 'first_name',)

    def __unicode__(self):
        return self.get_full_name()

    def gravatar_url(self):
        email_hash = hashlib.md5(self.email.strip().lower()).hexdigest()
        return 'http://www.gravatar.com/avatar/%s.jpg' % email_hash
