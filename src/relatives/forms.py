# -*- coding: utf-8 -*-

import re
import calendar

from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from src.relatives import models


DATE_HELP = u"""
Вводите данные в формате "DD.MM.YYYY".
Например, введите "*.*.1951", если месяц и день неизвестен.
"""

DATE_RE = re.compile('(?P<day>[\d\*]{1,2})[\.\/](?P<month>[\d\*]{1,2})[\.\/](?P<year>\d{4})')


class PersonForm(forms.ModelForm):
    birth = forms.CharField(u'Дата рождения', required=False,
        help_text=DATE_HELP, widget=AdminDateWidget)
    death = forms.CharField(u'Дата смерти', required=False,
        help_text=DATE_HELP, widget=AdminDateWidget)

    class Meta:
        model = models.Person
        exclude = (
            'birth_year', 'birth_month', 'birth_day',
            'death_year', 'death_month', 'death_day')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', dict())
            initial.update(dict(birth=instance.repr_birth(), death=instance.repr_death()))
            kwargs['initial'] = initial
        super(PersonForm, self).__init__(*args, **kwargs)

    def _clean_datefield(self, name):
        value = self.cleaned_data.get(name)
        year, month, day = None, None, None
        re_obj = DATE_RE.match(value)
        if re_obj:
            day, month, year = map(
                lambda x: int(x) if x.isdigit() else None,
                re_obj.groups())

            if month:
                if not 1 <= month <= 12:
                    raise forms.ValidationError(u'Проверьте месяц')

            if day:
                limit = 31
                if month:
                    weekday, days = calendar.monthrange(year, month)
                    limit = days
                if not 1 <= int(day) <= limit:
                    raise forms.ValidationError(u'Проверьте число месяца!')

        return (year, month, day)

    def clean(self):
        year, month, day = self._clean_datefield('birth')
        values = dict(birth_year=year, birth_month=month, birth_day=day)
        self.cleaned_data.update(values)

        year, month, day = self._clean_datefield('death')
        values = dict(death_year=year, death_month=month, death_day=day)
        self.cleaned_data.update(values)

        return self.cleaned_data

    def save(self, commit=True):
        instance = super(PersonForm, self).save(commit=commit)

        for field in self._meta.exclude:
            value = self.cleaned_data.get(field)
            setattr(instance, field, value)
        instance.save()
        return instance


class PersonRelationForm(forms.ModelForm):
    begin = forms.DateField(label=u'Началось', required=False,
        help_text=DATE_HELP, widget=AdminDateWidget)
    end = forms.DateField(label=u'Завершилось', required=False,
        help_text=DATE_HELP, widget=AdminDateWidget)

    class Meta:
        model = models.Person
        exclude = ('relation',
            'begin_year', 'begin_month', 'begin_day',
            'end_year', 'end_month', 'end_day')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', dict())
            initial.update(dict(begin=instance.repr_begin(), end=instance.repr_end()))
            kwargs['initial'] = initial
        super(PersonRelationForm, self).__init__(*args, **kwargs)
