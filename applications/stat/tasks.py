# -*- coding: utf-8 -*-
# __author__ = xutao

# 定义celery任务
from celery import task
from libs.datetimes import datetime_now
import uuid
from pyVmomi import vmodl, vim
from libs.vcenter import stat_vm_work, vm_to_template, add_template, datastore_info
from applications.stat.models import VmStat, Task, Vcenter
import logging
import traceback
import time
from datetime import datetime, timedelta
from libs.ovftool import create_ova
from libs.datetimes import datetime_to_str
from libs.vcenter import destroy_tpl


logger = logging.getLogger(__name__)

@task
def test_con(a, b):
    logger.info("yesyesyysysysysyysysys")
    time.sleep(20)
    return a+b


@task
def vm_stat(host, username, password, vm_name, vm_stat_id, stat_type="", start="", end=""):
    """
        统计 vm 的性能数据
    :return:
    """
    try:

        stat_data, filter_type = stat_vm_work(host=host, username=username, password=password, vm_name=vm_name, stat_type=stat_type,
                                 start=start, end=end)

        time_data = [start]

        day_timedelta = end - start
        hours_interval = day_timedelta.days * 24 / 9
        logger.debug(filter_type)

        if filter_type == "hours":
            for index, data in enumerate(range(5)):
                if index not in [0, 4]:
                    start = start + timedelta(hours=6)
                    time_data.append(start)
        else:

            for index, data in enumerate(range(10)):
                logger.debug("data")
                if index not in [0, 9]:
                    start = start + timedelta(hours=hours_interval)
                    time_data.append(start)

        time_data.append(end)

        time_data = [datetime_to_str(datetime_tmp, "%Y-%m-%d %H:%M:%S") for datetime_tmp in time_data]

        data = {
            "stat_data": stat_data,
            "time_data": time_data,
        }

        now_stat = VmStat.objects.get(id=vm_stat_id)
        now_stat.result = data
        now_stat.status = "success"
        now_stat.save()
    except Exception as e:
        logger.info("vm_stat when catch exception:%s" % traceback.format_exc())
        data = {
            "errormsg": str(traceback.format_exc())
        }
        vm_stat = VmStat(vm_name=vm_name, result=data, status="fault")
        vm_stat.save()


@task
def vm_to_tpl(host, username, password, vm_name, template_name, params, data_center, data_store, cluster, task_id,
              src_site_id, des_site_id, action_type):
    now_task = Task.objects.get(task_id=task_id)
    try:
        logger.info("start vm:%s to tpl:%s" % (vm_name, template_name))

        if action_type == "p2p":
            # 直接进行分发
            logger.info("vm_name:%s is just to p2p not ovftool" % template_name)
            now_task.status = "ovf_success"
            now_task.save()
            return 1

        if action_type == "test":
            # just for test
            logger.info("vm_name:%s is just to success" % vm_name)
            now_task.status = "success"
            now_task.save()
            return 1

        is_success = vm_to_template(host=host, username=username, password=password, vm_name=vm_name, template_name=template_name,
                                    datacenter_name=data_center, cluster=cluster, datastore=data_store)

        if is_success == 1:
            if src_site_id == des_site_id:
                logger.info("start to ova this tpl is %s" % template_name)
                vcenter = Vcenter.objects.get(site_id=src_site_id)
                status = create_ova(host=host, username=username, password=password, datacenter=data_center,
                                    vm_name=template_name, port=vcenter.ovf_agent_port,
                                    ovf_host=vcenter.ovf_agent_host, task_id=now_task.task_id)
                now_task.status = "start_ovf" if status else "ovf_fault"
                logger.info("req to create tpl: %s success" % template_name)
                # template_id = add_template(template_name, params)
                # logger.info("template_id is %s" % template_id)
                # now_task.result['template_id'] = template_id if template_id else "11111111111111"
                now_task.save()
                return 1
            else:
                # 开始转化为 ova 进行分发
                vcenter = Vcenter.objects.get(site_id=src_site_id)
                status = create_ova(host=host, username=username, password=password, datacenter=data_center, vm_name=template_name, port=vcenter.ovf_agent_port,
                                    ovf_host=vcenter.ovf_agent_host, task_id=now_task.task_id)
                now_task.status = "start_ovf" if status else "ovf_fault"
                now_task.save()
        else:
            now_task.status = "fault"
            now_task.save()
            return -1
    except vim.fault.InvalidPowerState:
        logger.info("vm_to_tpl when catch power state invalid:%s" % traceback.format_exc())
        now_task.status = "success"
        now_task.result['template_id'] = template_id if template_id else ""
        now_task.save()
    except Exception as e:
        logger.info("vm_to_tpl when catch exception:%s" % traceback.format_exc())
        now_task.status = "fault"
        now_task.result = {"errmsg": str(traceback.format_exc())}
        now_task.save()
        return -1


@task
def check_datastore_status():

    vcenters = Vcenter.objects.all()

    for vcenter in vcenters:
        logger.info("start update vcenter:%s datastor info" % vcenter.site)
        capacity, free_space = datastore_info(host=vcenter.host, password=vcenter.password, username=vcenter.username,
                                              datastore=vcenter.data_store)

        vcenter.capacity = capacity

        vcenter.free_space = free_space

        vcenter.save()

        logger.info("start update vcenter:%s datastor info that ca:%s free:%s" % (vcenter.site, capacity, free_space))

@task
def delete_tpl(tpl_name, task_id, site_id):
    """
        删除模板
    """
    site = Vcenter.objects.get(site_id=site_id)
    destroy_status, msg = destroy_tpl(host=site.host, username=site.username, password=site.password, tpl_name=tpl_name)
    task = Task.objects.get(task_id=task_id)

    if destroy_status:
        task.status = "success"
        task.result["status"] = "destroy tpl is success tpl:%s" % tpl_name
        task.save()
    else:

        task.status = "fault"

        task.result["status"] = msg

        task.save()

    logger.info("destroy tpl:%s is complete status:%s" % (tpl_name, task.status))




@task
def vm_to_tpl_new(host, username, password, vm_name, template_name, params, data_center, data_store, cluster, task_id,
                  src_site_id, des_site_id):
    """
        最新版模板,暂时没有用到
    :param host:
    :param username:
    :param password:
    :param vm_name:
    :param template_name:
    :param params:
    :param data_center:
    :param data_store:
    :param cluster:
    :param task_id:
    :param src_site_id:
    :param des_site_id:
    :return:
    """
    now_task = Task.objects.get(task_id=task_id)
    try:
        logger.info("start vm:%s to tpl:%s" % (vm_name, template_name))
        is_success = vm_to_template(host=host, username=username, password=password, vm_name=vm_name, template_name=template_name,
                                    datacenter_name=data_center, cluster=cluster, datastore=data_store)

        if is_success == 1:
            template_id = add_template(template_name, params)
            logger.info("template_id is %s" % template_id)
            if des_site_id == src_site_id:
                now_task.status = "success"
            else:
                now_task.status = "to_ova"
            now_task.result['template_id'] = template_id if template_id else "11111111111111"
            now_task.save()
            return 1
        else:
            now_task.status = "fault"
            now_task.save()
            return -1
    except vim.fault.InvalidPowerState:
        logger.info("vm_to_tpl when catch power state invalid:%s" % traceback.format_exc())
        now_task.status = "success"
        now_task.result['template_id'] = template_id
        now_task.save()
    except Exception as e:
        logger.info("vm_to_tpl when catch exception:%s" % traceback.format_exc())
        now_task.status = "fault"
        now_task.result = {"errmsg": str(traceback.format_exc())}
        now_task.save()
        return -1

@task
def test(sleep_time):
    print("yesys")
    time.sleep(2)
    return 1


def create_torrent(host, post, username, password, datacenter, vm_name, task_id):
    """
        创建种子
    :return:
    """
    pass