# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models

SEX = enumerate([u'Мужской', u'Женский', ])
REL_TYPE = enumerate([u'Приёмные родители', u'Брак', ''])
REN_TYPE = enumerate([u'Намерение', u'Брак'])


class Person(models.Model):
    father = models.ForeignKey('Person', related_name=u'my_father', null=True, blank=True)
    mother = models.ForeignKey('Person', related_name=u'my_mother', null=True, blank=True)
    fname = models.CharField(u'Фамилия', max_length=128, null=True, blank=True)
    iname = models.CharField(u'Имя', max_length=128, null=True, blank=True)
    oname = models.CharField(u'Отчество', max_length=128, null=True, blank=True)
    sex = models.IntegerField(u'Пол', choices=SEX)
    birth_year = models.IntegerField(u'Год рождения', null=True, blank=True)
    birth_month = models.IntegerField(u'Месяц рождения', null=True, blank=True)
    birth_day = models.IntegerField(u'День рождения', null=True, blank=True)
    death_year = models.IntegerField(u'Год смерти', null=True, blank=True)
    death_month = models.IntegerField(u'Месяц смерти', null=True, blank=True)
    death_day = models.IntegerField(u'День смерти', null=True, blank=True)
    relation = models.ManyToManyField('Person', related_name='children', through='Relation')

    class Meta:
        verbose_name = u'Человек'
        verbose_name_plural = u'Люди'
        ordering = ['birth_year', 'fname', 'iname', 'oname']

    def __unicode__(self):
        return u'%s: %s %s' % (self.birth_year, self.fname, self.iname)
        #return u'%s (%s)' % (self.fullname(), self.repr_lifetime)

    def fullname(self):
        return u' '.join(list(self.prepare_fields()))

    def shortname(self, just_name=True):
        fname, iname, oname = self.prepare_fields()
        if just_name:
            return u'%s %s' % (fname, iname)
        else:
            return u'%s %s.%s.' % (fname, iname[0], self.oname[0])

    def prepare_fields(self):
        fname = self.fname if self.fname is not None else u''
        iname = self.iname if self.fname is not None else u''
        oname = self.oname if self.fname is not None else u''
        return (fname, iname, oname)

    def _get_date(self, year, month, day):
        value = '%i.%i.%i' % (day, month, year)
        return datetime.strptime(value, '%d.%m.%Y').date()

    def get_birth(self):
        return self._get_date(self.birth_year, self.birth_month, self.birth_day)

    def get_death(self):
        return self._get_date(self.death_year, self.death_month, self.death_day)

    def repr_birth(self):
        u"""Возвращает строку с датой рождения"""
        if self.birth_year is not None:
            year = self.birth_year or u'*'
            month = self.birth_month or u'*'
            day = self.birth_day or u'*'
            return u'%s.%s.%s' % (day, month, year)
        else:
            return u''

    def repr_death(self):
        u"""Возвращает строку с датой смерти"""
        if self.death_year is not None:
            year = self.death_year or u'*'
            month = self.death_month or u'*'
            day = self.death_day or u'*'
            return u'%s.%s.%s' % (day, month, year)
        else:
            return u''

    def repr_lifetime(self):
        u"""Возвращает строку с годами жизни."""
        if any([self.death_year, self.death_month, self.death_day]):
            return u'%s - %s' % (self.repr_birth(), self.repr_death())
        else:
            return self.repr_birth()


class Relation(models.Model):
    src = models.ForeignKey('Person', related_name=u'related_src')
    dst = models.ForeignKey('Person', verbose_name=u'С кем', related_name=u'related_dst')
    begin_year = models.IntegerField(u'Год начала', null=True, blank=True)
    begin_month = models.IntegerField(u'Месяц начала', null=True, blank=True)
    begin_day = models.IntegerField(u'День начала', null=True, blank=True)
    end_year = models.IntegerField(u'Год завершения', null=True, blank=True)
    end_month = models.IntegerField(u'Месяц завершения', null=True, blank=True)
    end_day = models.IntegerField(u'День завершения', null=True, blank=True)
    otype = models.IntegerField(u'Связь', choices=REL_TYPE)

    class Meta:
        verbose_name = u'Отношение'
        verbose_name_plural = u'Отношения'

    def __unicode__(self):
        return self.get_otype_display()

    def _get_date(self, year, month, day):
        value = '%i.%i.%i' % (year, month, day)
        return datetime.strptime(value, '%d.%m.%Y').date()

    def get_begin(self):
        return self._get_date(self.begin_year, self.begin_month, self.begin_day)

    def get_end(self):
        return self._get_date(self.end_year, self.end_month, self.end_day)

    def repr_begin(self):
        u"""Возвращает строку с датой начала связи"""
        if self.begin_year is not None:
            year = self.begin_year or u'*'
            month = self.begin_month or u'*'
            day = self.begin_day or u'*'
            return u'%s.%s.%s' % (day, month, year)
        else:
            return u''

    def repr_end(self):
        u"""Возвращает строку с датой завершения связи"""
        if self.end_year is not None:
            year = self.end_year or u'*'
            month = self.end_month or u'*'
            day = self.end_day or u'*'
            return u'%s.%s.%s' % (day, month, year)
        else:
            return u''

    def repr_duration(self):
        u"""Возвращает строку с датами начала и завершения связи."""
        if any([self.end_year, self.end_month, self.end_day]):
            return u'%s - %s' % (self.repr_begin(), self.repr_end())
        else:
            return self.repr_begin()


class Rename(models.Model):
    person = models.ForeignKey(Person, related_name='renames')
    fname = models.CharField(u'Фамилия', max_length=128, null=True, blank=True)
    iname = models.CharField(u'Имя', max_length=128, null=True, blank=True)
    oname = models.CharField(u'Отчество', max_length=128, null=True, blank=True)
    occurred = models.DateTimeField(u'Произошло')
    reason = models.IntegerField(u'Причина', choices=REN_TYPE)
