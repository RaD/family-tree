# -*- coding: utf-8 -*-

from django.contrib import admin

from src.relatives import models
from src.relatives import forms


class PersonRelationInline(admin.TabularInline):
    form = forms.PersonRelationForm
    model = models.Relation
    fk_name = 'src'


class BrotherRelationInline(admin.TabularInline):
    model = models.Person
    fk_name = 'father'

    def queryset(self, request):
        qs = super(BrotherRelationInline, self).queryset(request)
        #import pdb; pdb.set_trace()
        return qs


class Person(admin.ModelAdmin):
    list_display = ('fullname', 'lifetime', 'sex', )
    form = forms.PersonForm
    inlines = (PersonRelationInline, )  # BrotherRelationInline)

    def fullname(self, obj):
        return obj.fullname()

    def lifetime(self, obj):
        return obj.repr_lifetime()

admin.site.register(models.Person, Person)


class Relation(admin.ModelAdmin):
    list_display = ('src', 'dst', 'duration', 'otype', )
    form = forms.PersonRelationForm

    def duration(self, obj):
        return obj.repr_duration()
