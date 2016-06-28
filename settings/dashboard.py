# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function

from grappelli.dashboard import modules, Dashboard
from djcelery import models
from djcelery.models import WorkerState


class CustomIndexDashboard(Dashboard):
    title = u"gic 运维后台"

    def init_with_context(self, context):
        site_name = u"运维后台"

        self.children.append(modules.ModelList(
            u"表单管理",
            column=1,
            collapsible=True,
            models=(
                'applications.users.models.User',
                'applications.stat.models.VmStat',
                'applications.stat.models.Vcenter',
                'applications.stat.models.Task',
            )
        ))

        self.children.append(modules.ModelList(
                u"任务调度器",
                column=1,
                collapsible=True,
                models=(
                    'djcelery.models.PeriodicTask',
                    "djcelery.models.WorkerState",
                    "kombu.transport.django.models.Message",
                )
            ))