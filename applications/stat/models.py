# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function

import decimal
from django.db import models
from django.conf import settings
from django_extensions.db.fields.json import JSONField
from libs.datetimes import datetime_now
from datetime import datetime

import json

import logging

from libs.ovftool import deploy_ova

logger = logging.getLogger(__name__)

TASK_STATUS = (
        ('creating', u'创建',),
        ('success', u'成功',),
        ('doing', u'执行中',),
        ('fault', u'失败',),
        ("start_ovf", "开始ovf"),
        ("ovf_fault", u"ovf失败"),
        ("ovf_success", u"ovf成功"),
        ("start_torrent", u"生成种子"),
        ("torrent_success", u"生成种子成功"),
        ("torrent_fault", u"生成种子失败"),
        ("start_p2p", "开始分发"),
        ("p2p_fault", "分发失败"),
        ("p2p_success", "分发成功"),
        ("start_deploy", "开始部署"),
        ("deploy_fault", u"部署失败"),
        ("deploy_success", u"部署成功"),
        ("start_del_tpl", u"开始删除模板"),
        ("error_del_tpl", u"删除模板失败"),
        ("success_del_tpl", u"删除模板失败"),

    )


class VmStat(models.Model):
    class Meta:
        db_table = "vm_stat"
        app_label = "stat"
        verbose_name = verbose_name_plural = u"虚拟机性能"

    vm_name = models.CharField(u"虚拟机名称", max_length=1024, null=True, blank=True)
    data = JSONField(u"详细信息", blank=True, null=True)
    result = JSONField(u"结果", blank=True, null=True)
    status = models.CharField(u"任务状态", choices=TASK_STATUS, default="creating", max_length=16)
    created_at = models.DateTimeField(u"创建时间", blank=True, null=True, default=datetime_now())

    def __unicode__(self):
        return self.vm_name

    def decimal_default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError

    def to_json(self):
        json_tmp = json.dumps({
            "vm_name": self.vm_name,
            "result": self.result,
            "status": self.status,
        }, default=self.decimal_default)
        return json.loads(json_tmp)


class Vcenter(models.Model):
    class Meta:
        db_table = "vcenter_info"
        app_label = "stat"
        verbose_name = verbose_name_plural = u"数据中心"
    site_id = models.CharField(u"pod id", max_length=36, null=True, blank=True)
    site = models.CharField(u"pod name", max_length=32, null=True, blank=True)
    host = models.CharField(u"host", max_length=16, null=True, blank=True)
    username = models.CharField(u"用户名", max_length=32, null=True, blank=True)
    password = models.CharField(u"密码", max_length=32, null=True, blank=True)
    data_center = models.CharField(u"数据中心", max_length=32, null=True, blank=True)
    data_store = models.CharField(u"存储卷", max_length=32, null=True, blank=True)
    cluster_name = models.CharField(u"群集", max_length=32, blank=True, null=True)


    # ovftool 相关
    ovf_agent_host = models.CharField(u"ovf agent ip", max_length=16, null=True, blank=True)
    ovf_agent_port = models.IntegerField(u"ovf agent port", null=True, blank=True, default=9999)

    # 分发网络控制节点
    p2p_center_host = models.CharField(u"p2p center ip", max_length=16, null=True, blank=True)
    p2p_center_port = models.IntegerField(u"p2p center port", null=True, blank=True, default=9091)

    tpl_folder = models.CharField(u"pod tpl folder", max_length=32, null=True, blank=True)

    capacity = models.FloatField(u"总容量", null=True, blank=True)     # 单位 GB

    free_space = models.FloatField(u"可用容量", null=True, blank=True)   # 单位 GB

    def __unicode__(self):
        return self.site

    def can_tpl(self):
        """
            是否可以进行模板操作
        :return:
        """
        if self.free_space < 100:
            # 小于 100 G 需要预警
            return False
        return True

from settings.const import OVA_PATH, TORRENT_DOWNLOAD_DIR
import requests


class Task(models.Model):
    class Meta:
        db_table = "vcenter_task"
        app_label = "stat"
        verbose_name = verbose_name_plural = u"任务"

    task_id = models.CharField(u"任务id", null=True, blank=True, max_length=64)
    params = JSONField(u"参数", blank=True, null=True)
    result = JSONField(u"结果", blank=True, null=True)
    status = models.CharField(u"任务状态", choices=TASK_STATUS, default="creating", max_length=16)
    created_at = models.DateTimeField(u"创建时间", blank=True, null=True, default=datetime_now())

    def __unicode__(self):
        return self.task_id

    def to_json(self):
        return {
            "task_id": self.task_id,
            "status": self.status,
            "result": self.result,
        }

    def start_deploy(self):
        """
            开始部署
        :return:
        """
        des_site_id = self.params["des_site_id"]
        des_vcenter = Vcenter.objects.get(site_id=des_site_id)
        host = des_vcenter.host
        username = des_vcenter.username
        password = des_vcenter.password
        vm_name = self.params["template_name"]
        datastore = des_vcenter.data_store,
        datacenter = des_vcenter.data_center
        tpl_folder = des_vcenter.tpl_folder
        cluster_name = des_vcenter.cluster_name
        ovf_agent_port = des_vcenter.ovf_agent_port
        ovf_agent_host = des_vcenter.ovf_agent_host
        result = deploy_ova(host=host, port=ovf_agent_port, username=username, password=password, vm_name=vm_name,
                   datastore=datastore, datacenter=datacenter, tpl_folder=tpl_folder, cluster_name=cluster_name,
                            ovf_host=ovf_agent_host, task_id=self.task_id)
        if result:
            return True
        return False

    def start_distribute(self):
        """
            开始进行分发
        :return:
        """
        ova_path = "%s/%s.ova" % (OVA_PATH, self.params["template_name"])
        src_site_id = self.params["src_site_id"]
        des_site_id = self.params["des_site_id"]
        task_id = self.task_id
        vm_name = self.params["template_name"]
        site = Vcenter.objects.get(site_id=src_site_id)
        p2p_center_url = "http://%s:%s/distribute/" % (site.p2p_center_host, site.p2p_center_port)
        logger.info("p2p center:%s is %s distrite %s" % (site.p2p_center_host, site.p2p_center_port, vm_name))
        data = {
            "ova_path": ova_path,
            "src_site_id": src_site_id,
            "des_site_id": des_site_id,
            "task_id": task_id,
            "vm_name": vm_name
        }

        response = requests.post(p2p_center_url, data=data)
        if response.ok:
            result = response.json()
            if int(result["status"]) == 200:
                logger.info("vm:%s start p2p success" % vm_name)
                return True
        logger.info("vm:%s start p2p error:%s" % (vm_name, response.content))

        return False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.status == "ovf_success":
            # 开始 p2p 分发
            success = self.start_distribute()
            if not success:
                self.status = "fault"

        elif self.status == "ovf_fault":
            # ovf 错误
            self.status = "fault"

        elif self.status == "p2p_success":
            # 开始部署
            success = self.start_deploy()
            if not success:
                self.status = "fault"

        elif self.status == "deploy_success":
            # to add tpl to core
            self.status = "success"

        elif self.status == "deploy_fault":
            self.status = "fault"

        elif self.status == "torrent_fault":
            self.status = "fault"

        elif self.status == "p2p_fault":
            self.status = "fault"

        return super(Task, self).save(force_insert, force_update, using, update_fields)
