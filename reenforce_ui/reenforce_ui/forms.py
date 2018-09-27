# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
import datetime as dt
from django.forms.formsets import BaseFormSet, formset_factory

from bootstrap3.tests import TestForm

RADIO_CHOICES = (("1", "Radio 1"), ("2", "Radio 2"))

MEDIA_CHOICES = (
    ("Audio", (("vinyl", "Vinyl"), ("cd", "CD"))),
    ("Video", (("vhs", "VHS Tape"), ("dvd", "DVD"))),
    ("unknown", "Unknown"),
)

class LoginForm(forms.Form):
    your_name = forms.CharField(label='Your name: ', max_length=100)
    email_id = forms.EmailField(label='Email id: ', max_length=100)
    affil = forms.CharField(label='Affiliation: ', max_length=100)
    pass

class QueryForm(forms.Form):
    radar_code = forms.CharField(label='Radar Code: ', max_length=3, initial='fhe')
    date = forms.DateField(initial=dt.date(2012,5,1),label='Date: ')
    pass


class ContactForm(TestForm):
    pass


class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non form errors styling"
        )


ContactFormSet = formset_factory(
    TestForm, formset=ContactBaseFormSet, extra=2, max_num=4, validate_max=True
)


class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file5 = forms.ImageField()
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling."
        )
        return cleaned_data
