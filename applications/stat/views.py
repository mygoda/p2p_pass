# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function
from django.views.generic import View
from applications.stat.models import Vcenter, VmStat, Task
from applications.stat.tasks import vm_stat, vm_to_tpl, test, test_con
from libs.http import json_error_response, json_success_response, task_error_response
from libs.mixins.view import CsrfExemptMixin
import json
import re
from datetime import datetime
import pytz
from settings.const import OVF_TOKEN, CALLBACK_TOKEN

from applications.stat.tasks import delete_tpl

import logging

class VmNewStatView(CsrfExemptMixin, View):
    """
        new for us
    """

    def post(self, request, *args, **kwargs):
        data = request.POST
        vm_name = data.get("vm_name")
        vm_names = vm_name.split(",")
        pod_name = data.get("pod_name")
        site = Vcenter.objects.get(site=pod_name)
        host = site.host
        username = site.username
        password = site.password
        stat_item = VmStat(vm_name=vm_name, data={
            "pod_name": pod_name
        })
        stat_item.save()
        now_stat_id = stat_item.id
        vm_stat.delay(host=host, username=username, password=password, vm_name=vm_names, vm_stat_id=now_stat_id, stat_type="new")
        json_data = {
            "stat_id": now_stat_id
        }

        return json_success_response(json_data=json_data)

    def get(self, request, *args, **kwargs):
        vm_stat = VmStat.objects.get(**kwargs)
        data = vm_stat.to_json()
        return json_success_response(json_data=data)


class VmStatView(CsrfExemptMixin, View):

    def get_date(self, date_str):
        date_list = date_str.split(".")
        year = int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])
        utc = pytz.UTC
        return utc.localize(datetime(year=year, month=month, day=day, second=0, minute=0, hour=0))

    def post(self, request, *args, **kwargs):
        data = request.POST
        vm_name = data.get("vm_name")
        pod_name = data.get("pod_name")
        stat_type = ""
        date_to = data.get("date_to")
        date_from = data.get("date_from")

        start = self.get_date(date_from)
        end = self.get_date(date_to)
        site = Vcenter.objects.get(site=pod_name)
        host = site.host
        username = site.username
        password = site.password
        stat_item = VmStat(vm_name=vm_name, data={
            "pod_name": pod_name
        })
        stat_item.save()
        now_stat_id = stat_item.id
        vm_stat.delay(host=host, username=username, password=password, vm_name=vm_name, vm_stat_id=now_stat_id,
                      start=start,
                      end=end, stat_type=stat_type)
        json_data = {
            "stat_id": now_stat_id
        }

        return json_success_response(json_data=json_data)

    def get(self, request, *args, **kwargs):
        vm_stat = VmStat.objects.get(**kwargs)
        data = vm_stat.to_json()
        return json_success_response(json_data=data)


class TemplateBodyView(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        vm_name = data.get("vm_name")
        task_id = data.get("task_id")
        template_name = data.get("template_name")
        src_site_id = data.get("src_site_id")
        des_site_id = data.get("des_site_id")
        src_site = Vcenter.objects.get(site_id=src_site_id)
        host = src_site.host
        username = src_site.username
        password = src_site.password
        customer_id = data.get("customer_id")
        action = data.get("action_type")
        params = {
            "os_type": data.get("os_type"),
            "os_version": data.get("os_version"),
            "os_bit": data.get("os_bit"),
            "cpu": data.get("cpu"),
            "ram": data.get("mem"),
            "disk": data.get("disk"),
            "username": data.get("username"),
            "password": data.get("password"),
            "customer_id":customer_id
        }
        data = {
            "task_id": task_id,
            "vm_name": vm_name,
            "src_site_id": src_site_id,
            'des_site_id': des_site_id,
            "customer_id": customer_id
        }

        task = Task(task_id=task_id, params=data)
        task.save()
        vm_to_tpl.delay(vm_name=vm_name, host=host, username=username, password=password, template_name=template_name,
                        task_id=task_id, params=params, data_center=src_site.data_center,
                        data_store=src_site.data_store, cluster=src_site.cluster_name, src_site_id=src_site_id, des_site_id=des_site_id, action_type=action)
        data = task.to_json()
        return json_success_response(json_data=data)


class TaskView(CsrfExemptMixin, View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        if task_id.endswith("/"):
            kwargs["task_id"] = task_id[:-1]
        task = Task.objects.get(**kwargs)
        data = task.to_json()

        if task.status == "fault":
            return json_error_response(json_data=data, msg=u"task is error")
        else:
            return json_success_response(json_data=data)


class TestView(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        import json
        return json_success_response(json_data=data)

    def get(self, request, *args, **kwargs):
        test_con.delay(1,6)
        # # return json_success_response(json_data={"data": "hello"})
        return json_error_response(json_data={"hello": "data"}, msg="hello")


class OvftoolView(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        token = data.get("token")
        if token != OVF_TOKEN:
            return json_error_response(json_data={}, msg="can not use this")
        task_id = data.get("task_id")
        task = Task.objects.get(task_id=task_id)
        task.status = data.get("status")
        task.save()
        return json_success_response(json_data=data)


class TemplateDelteView(CsrfExemptMixin, View):
    """
        模板删除处理
    """
    def post(self, request, *args, **kwargs):
        """
            删除模板功能
        :return:
        """
        data = request.POST
        task = Task(task_id=data.get("task_id"), params=data, status="start_del_tpl")
        task.save()
        delete_tpl.delay(tpl_name=data.get("template_name"), task_id=data.get("task_id"), site_id=data.get("site_id"))
        logging.info("task:%s delete tpl is start" % task.task_id)

        return json_success_response(json_data=data)


class NewTemplateView(CsrfExemptMixin, View):
    """
        新版模板处理
    """

    def post(self, request, *args, **kwargs):
        data = request.POST
        vm_name = data.get("vm_name")
        task_id = data.get("task_id")
        template_name = data.get("template_name")
        src_site_id = data.get("src_site_id")
        des_site_id = data.get("des_site_id")
        src_site = Vcenter.objects.get(site_id=src_site_id)
        des_site = Vcenter.objects.get(site_id=des_site_id)
        if not des_site.can_tpl() and not src_site.can_tpl():

            result = {"msg": u"源平台/目的平台 vcenter 模板存储空间小于100G, 不能创建模板 src:%s, des:%s" % (src_site_id, des_site_id)}

            task = Task(task_id=task_id, params=data, status="fault", result=result)
            task.save()

            return json_success_response(json_data=task.to_json())

        host = src_site.host
        username = src_site.username
        password = src_site.password
        customer_id = data.get("customer_id")
        action = data.get("action_type")
        params = {
            "os_type": data.get("os_type"),
            "os_version": data.get("os_version"),
            "os_bit": data.get("os_bit"),
            "cpu": data.get("cpu"),
            "ram": data.get("mem"),
            "disk": data.get("disk"),
            "username": data.get("username"),
            "password": data.get("password"),
            "customer_id":customer_id
        }
        data = {
            "task_id": task_id,
            "vm_name": vm_name,
            "src_site_id": src_site_id,
            'des_site_id': des_site_id,
            "customer_id": customer_id,
            "template_name": template_name,
            "params": params,
        }

        task = Task(task_id=task_id, params=data)
        task.save()
        vm_to_tpl.delay(vm_name=vm_name, host=host, username=username, password=password, template_name=template_name,
                        task_id=task_id, params=params, data_center=src_site.data_center,
                        data_store=src_site.data_store, cluster=src_site.cluster_name, src_site_id=src_site_id, des_site_id=des_site_id, action_type=action)

        data = task.to_json()
        return json_success_response(json_data=data)


class TaskCallbackView(CsrfExemptMixin, View):
    """
        任务成功,失败与否的回调
    """

    def post(self, request, *args, **kwargs):
        data = request.POST
        # 完成回调
        task_id = data.get("task_id")
        result = data.get("result")
        status = data.get("status")
        task = Task.objects.get(task_id=task_id)
        task.result["status"] = result
        task.status = status
        task.save()
        return json_success_response(json_data={})

