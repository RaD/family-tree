# -*- coding: utf-8 -*-

import re
import calendar

from django.db import models


DATE_HELP = u"""
Вводите данные в формате "DD.MM.YYYY".
Например, введите "xx.xx.1951", если месяц и день неизвестен.
"""

DATE_RE = re.compile('(?P<day>[\d\*]{1,2})\.(?P<month>[\d\*]{1,2})\.(?P<year>\d{4})')


class FuzzyDateField(models.Field):
    u"""Класс поля с нечёткой датой."""

    description = FuzzyDateField.__doc__

    __metaclass__ = models.SubcfieldBase

    def to_python(self, value):
        re_obj = DATE_RE.match(self.cleaned_data.get('birth'))
        if re_obj:
            year = re_obj.group('year')
            month = re_obj.group('month')
            day = re_obj.group('day')

            year = int(year)
            month = int(month) if month.isdigit() else None
            day = int(day) if day.isdigit() else None

            if month:
                if not 1 <= month <= 12:
                    raise ValueError(u'Проверьте месяц')

            if day:
                limit = 31
                if month:
                    weekday, days = calendar.monthrange(year, month)
                    limit = days
                if not 1 <= int(day) <= limit:
                    raise ValueError(u'Проверьте число месяца!')

        return (year, month, day)

    def get_prep_value(self, value):
        pass
