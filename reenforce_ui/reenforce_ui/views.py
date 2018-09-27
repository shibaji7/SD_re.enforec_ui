# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.core.files.storage import default_storage
import datetime as dt

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
import json

from .forms import ContactForm, FilesForm, ContactFormSet, LoginForm, QueryForm
from .models import *


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, "dummy.txt")


class HomePageView(TemplateView):
    template_name = "reenforce_ui/home.html"
    print(template_name)
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context


class DefaultFormsetView(FormView):
    template_name = "reenforce_ui/formset.html"
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = "reenforce_ui/form.html"
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = "reenforce_ui/form_by_field.html"
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = "reenforce_ui/form_horizontal.html"
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = "reenforce_ui/form_inline.html"
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = "reenforce_ui/form_with_files.html"
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", "vertical")
        return context

    def get_initial(self):
        return {"file4": fieldfile}


class PaginationView(TemplateView):
    template_name = "reenforce_ui/pagination.html"

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append("Line %s" % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get("page")
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context["lines"] = show_lines
        return context


class MiscView(TemplateView):
    template_name = "reenforce_ui/misc.html"


##
# Page Implementation
##
class LoginPageView(TemplateView):
    template_name = "reenforce_ui/login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        messages.info(self.request, "Login Required")
        return context

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            query = "?" + "name="+form.data['your_name'] + "&email="+ form.data['email_id'] +"&affil="+ form.data['affil']
            return HttpResponseRedirect('/query'+query)
        return render(request, self.template_name, {'form': form})

class QueryPageView(TemplateView):
    template_name = "reenforce_ui/query.html"
    form_class = QueryForm
    
    def get(self, request):
        try:
            return render(request, self.template_name, { 'email': request.GET.get("email"), "dt":"2012-05-01", "rad":"fhe"})
        except:
            return HttpResponseRedirect('/')

def get_data(request):
    try:
        email = request.GET.get("email")
        date = dt.datetime.strptime(request.GET.get("dt"),"%Y-%m-%d")
        radar = request.GET.get("rad")
        df = get_one_day_data(date, rad=radar)
        print(df.head())
        data = df.to_json().replace('},{', '} {')
        return HttpResponse(data, content_type='application/json')
    except:
        return HttpResponse("{message: System exception!!}", content_type='application/json')
