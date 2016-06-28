# -*- coding: utf-8 -*-
# __author__ = xutao

import requests
from settings.const import TOKEN, OVF_TOKEN
import logging

logger = logging.getLogger(__name__)


def create_ova(host, port, username, password, datacenter, vm_name, task_id, ovf_host):
    """
        创建 ova 文件
    :return:
    """
    data = {
        "host": host,
        "username": username,
        "password": password,
        "token": OVF_TOKEN,
        "datacenter": datacenter,
        "vm_name": vm_name,
        "task_id": task_id
    }

    url = "http://%s:%s/api/ovas/" % (ovf_host, port)
    print(url)
    print(data)
    respone = requests.post(url, data=data)
    print(respone.content)
    if respone.ok:
        json_data = respone.json()
        if json_data.get("status") == "ok":
            logger.info("just convert to ova success vm:%s" % vm_name)
            return True
        else:
            logger.info("convert to ova forbid token is invalid vm:%s" % vm_name)
            return False
    logger.info("server is not work just for 500 vm:%s" % vm_name)
    return False


def deploy_ova(host, port, username, password, datacenter, vm_name, datastore, cluster_name, tpl_folder, task_id, ovf_host):
    """
        部署 ova
    :param host:
    :param port:
    :param username:
    :param password:
    :param datacenter:
    :param vm_name:
    :param datastore:
    :param cluster_name:
    :param task_id:
    :return:
    """
    data = {
        "host": host,
        "username": username,
        "password": password,
        "token": OVF_TOKEN,
        "datacenter": datacenter,
        "vm_name": vm_name,
        "cluster_name": cluster_name,
        "task_id": task_id,
        "datastore": datastore,
        "tpl_folder": tpl_folder,
    }

    url = "http://%s:%s/api/vms/" % (ovf_host, port)
    print(url)
    respone = requests.post(url, data=data)
    print(respone.content)
    if respone.ok:
        json_data = respone.json()
        if json_data.get("status") == "ok":
            logger.info("just delpoy ova success vm:%s" % vm_name)
            return True
        else:
            logger.info("deploy ova forbid token is invalid vm:%s" % vm_name)
            return False
    logger.info("server is not work just for 500 vm:%s" % vm_name)
    return False