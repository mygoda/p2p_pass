# -*- coding: utf-8 -*-
# __author__ = xutao
from __future__ import division, unicode_literals, print_function
from django.contrib import admin

from applications.stat.models import VmStat, Vcenter,Task


# class VcenterAdmin(admin.ModelAdmin):
#
#     list_display = ["site"]
#
#
# class VmStatAdmin(admin.ModelAdmin):
#
#     list_display = ["vm_name"]

admin.site.register(VmStat)
admin.site.register(Vcenter)
admin.site.register(Task)
