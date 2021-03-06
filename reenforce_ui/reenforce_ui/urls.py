# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path

from .views import (
    LoginPageView,
    QueryPageView,
    HomePageView,
    FormHorizontalView,
    FormInlineView,
    PaginationView,
    FormWithFilesView,
    DefaultFormView,
    MiscView,
    DefaultFormsetView,
    DefaultFormByFieldView,
    get_data,
)

urlpatterns = [
    url(r"^$", LoginPageView.as_view(), name="login"),
    url(r"^query$", QueryPageView.as_view(), name="query"),
    path("data", get_data, name="data"),
    url(r"^formset$", DefaultFormsetView.as_view(), name="formset_default"),
    url(r"^form$", DefaultFormView.as_view(), name="form_default"),
    url(r"^form_by_field$", DefaultFormByFieldView.as_view(), name="form_by_field"),
    url(r"^form_horizontal$", FormHorizontalView.as_view(), name="form_horizontal"),
    url(r"^form_inline$", FormInlineView.as_view(), name="form_inline"),
    url(r"^form_with_files$", FormWithFilesView.as_view(), name="form_with_files"),
    url(r"^pagination$", PaginationView.as_view(), name="pagination"),
    url(r"^misc$", MiscView.as_view(), name="misc"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
