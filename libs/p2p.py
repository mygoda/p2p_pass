# -*- coding: utf-8 -*-
# __author__ = xutao

import requests
from settings.const import P2P_CENTER_HOST, OVA_PATH
import logging

logger = logging.getLogger(__name__)


def create_torrent(site_id, vm_name, task_id):
    """
        创建种子接口
    :return:
    """

    url = "http://%s/%s/" % (P2P_CENTER_HOST, "torrents")

    ova_path = "%s/%s.ova" % (OVA_PATH, vm_name)

    data = {
        "site_id": site_id,
        "path": ova_path,
        "comment": vm_name,
        "name": vm_name,
        "task_id": task_id,
    }

    response = requests.post(url, data=data)
    if response.ok:
        logger.info("create vm:%s torrent file has response:%s" % (vm_name, response.json()))
        return True
    return False
