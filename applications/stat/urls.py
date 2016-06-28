# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function
from django.conf.urls import patterns, url
from applications.stat.views import VmStatView, NewTemplateView, TestView, TaskView, VmNewStatView, OvftoolView,\
    TaskCallbackView, TemplateBodyView, TemplateDelteView
from settings.const import TASK_ID, URL_ID

urlpatterns = patterns('',
    url(r'^vms/?$', VmStatView.as_view(), name="vms_view"),
    url(r'^templates/?$', NewTemplateView.as_view(), name="templates_view"),
    url(r'^templates/del/?$', TemplateDelteView.as_view(), name="templates_delete_view"),
    url(r'^templates/json/?$', TemplateBodyView.as_view(), name="templates_json_view"),
    url(r'^vms/%s/?$' % URL_ID, VmStatView.as_view(), name="vm_stat_view"),
    url(r'^tasks/%s/?$' % TASK_ID, TaskView.as_view(), name="task_view"),
    url(r'^task/callback/?$', TaskCallbackView.as_view(), name="task_callback_view"),
    url(r'^test/?$', TestView.as_view(), name="test_view"),
    url(r"^new/vms/?$", VmNewStatView.as_view(), name="stat_new_view"),
    url(r"^ovftool/?$", OvftoolView.as_view(), name="ovftool_view"),
)