# -*- coding: utf-8 -*-
# __author__ = xutao
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl, vim
from datetime import timedelta, datetime
import uuid
import json
import time
import ssl
import requests
from django.conf import settings
from settings import settings
import logging
CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
CONTEXT.verify_mode = ssl.CERT_NONE

logger = logging.getLogger(__name__)

# something job in vcenter code here
def get_objs(content, vimtype):
    objs = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    objs = [vm for vm in container.view]

    return objs


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def waittask(task, actionName='job', hideResult=False):

    while task.info.state == vim.TaskInfo.State.running or task.info.state == vim.TaskInfo.State.queued:
        logger.info("task status is %s" % task.info.state)
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        logger.info("task is success")
        if task.info.result is not None and not hideResult:
            return task.info.result
    else:
        if task.info.error is not None:
            raise task.info.error


def BuildQuery(content, vchtime, counterId, instance, vm, interval, end=1):
    perfManager = content.perfManager
    metricId = vim.PerformanceManager.MetricId(counterId=counterId, instance=instance)
    startTime = vchtime - timedelta(hours=(interval + 1))
    endTime = vchtime - timedelta(hours=end)
    query = vim.PerformanceManager.QuerySpec(intervalId=300, entity=vm, metricId=[metricId], startTime=startTime,
                                             endTime=endTime)
    perfResults = perfManager.QueryPerf(querySpec=[query])
    if perfResults:
        return perfResults
    else:
        return False


def PrintVmInfo(vm, content, vchtime, interval, perf_dict, end=None, stat_type="cpu"):
    logger.info("just print vm info data")
    summary = vm.summary

    # is percentage
    statCpuUsage = BuildQuery(content, vchtime, (StatCheck(perf_dict, 'cpu.usage.average')), "", vm, interval, end)
    cpu_usage_list = statCpuUsage[0].value[0].value
    cpu_usage = [float(cpu) / 100 for cpu in cpu_usage_list]

    mem_all = float(summary.runtime.host.summary.hardware.memorySize) / 1024 / 1024 / 1024
    statMemoryActive = BuildQuery(content, vchtime, (StatCheck(perf_dict, 'mem.active.average')), "", vm, interval, end)
    memory_active_list = statMemoryActive[0].value[0].value
    memory_active = [float(mem) / 1024 / mem_all * 100 for mem in memory_active_list]
    disk_read = BuildQuery(content, vchtime, (StatCheck(perf_dict, 'virtualDisk.read.average')),
                                 "*", vm, interval, end)
    disk_read_stat = disk_read[0].value[0].value

    disk_write = BuildQuery(content, vchtime, (StatCheck(perf_dict, 'virtualDisk.write.average')),
                                     "*", vm, interval, end)
    disk_write_stat = disk_write[0].value[0].value

    data = {
        "cpu": cpu_usage,
        "disk_read": disk_read_stat,
        "disk_write": disk_write_stat,
        "mem": memory_active
    }
    return data


def StatCheck(perf_dict, counter_name):
    counter_key = perf_dict[counter_name]
    return counter_key


def GetProperties(content, viewType, props, specType):
    # Build a view and get basic properties for all Virtual Machines
    objView = content.viewManager.CreateContainerView(content.rootFolder, viewType, True)
    tSpec = vim.PropertyCollector.TraversalSpec(name='tSpecName', path='view', skip=False, type=vim.view.ContainerView)
    pSpec = vim.PropertyCollector.PropertySpec(all=False, pathSet=props, type=specType)
    oSpec = vim.PropertyCollector.ObjectSpec(obj=objView, selectSet=[tSpec], skip=False)
    pfSpec = vim.PropertyCollector.FilterSpec(objectSet=[oSpec], propSet=[pSpec], reportMissingObjectsInResults=False)
    retOptions = vim.PropertyCollector.RetrieveOptions()
    totalProps = []
    retProps = content.propertyCollector.RetrievePropertiesEx(specSet=[pfSpec], options=retOptions)
    totalProps += retProps.objects
    while retProps.token:
        retProps = content.propertyCollector.ContinueRetrievePropertiesEx(token=retProps.token)
        totalProps += retProps.objects
    objView.Destroy()
    # Turn the output in retProps into a usable dictionary of values
    gpOutput = []
    for eachProp in totalProps:
        propDic = {}
        for prop in eachProp.propSet:
            propDic[prop.name] = prop.val
        propDic['moref'] = eachProp.obj
        gpOutput.append(propDic)
    return gpOutput


def connect_vcenter(host, username, password):
    si = SmartConnect(host=host, user=username, pwd=password, port=443, sslContext=CONTEXT)
    return si


def stat_vm_work(host, username, password, vm_name, start=None, end=None, stat_type="cpu"):
    filter_type = "hours"
    day_delta = end - start
    if day_delta.days > 1:
        filter_type = "days"
    si = connect_vcenter(host=host, username=username, password=password)
    content = si.content
    vchtime = si.CurrentTime()
    interval = 24
    end_interval = 1
    if vchtime != end and end < vchtime:
        end_datetime = end
        seconds_delta = vchtime - end_datetime
        end_interval = seconds_delta.seconds / 60 / 60

    if vchtime > start:
        start_datetime = start
        seconds_delta = vchtime - start_datetime
        interval = seconds_delta.seconds / 60 / 60

    perf_dict = {}
    perfList = content.perfManager.perfCounter
    for counter in perfList:
        counter_full = "{}.{}.{}".format(counter.groupInfo.key, counter.nameInfo.key, counter.rollupType)
        perf_dict[counter_full] = counter.key

    retProps = GetProperties(content, [vim.VirtualMachine], ['name', 'runtime.powerState'], vim.VirtualMachine)

    for vm in retProps:
        if (vm['name'] in vm_name) and (vm['runtime.powerState'] == "poweredOn"):
            data_stat = PrintVmInfo(vm['moref'], content, vchtime, interval, perf_dict, end_interval, stat_type)
            logger.info(data_stat)
            for key, value in data_stat.items():
                data = filter_stat_data(value, filter_type)
                data_stat[key] = data
            logger.info(filter_type)
            return data_stat, filter_type
        elif vm['name'] in vm_name:
            logger.info('ERROR: Problem connecting to Virtual Machine.  {} is likely powered off or suspended'.format(vm['name']))
            return False
    if si:
        logger.info("delete vcenter connect")
        sock = si._stub.pool[0][0]._wrapped.sock
        sock.close()


def check_vm_status(vm_obj):
    """
        判断 vm 状态,如果是开机状态就给关机
    :param vm_obj:
    :return:
    """
    logger.info("start check vm_status")
    if vm_obj.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        task = vm_obj.PowerOffVM_Task()
        waittask(task, "poweroff vm task")
        return True
    else:
        return False


def op_vm(vm_obj, action):
    if action == "off":
        logger.info("start off vm")
        task = vm_obj.PowerOffVM_Task()
        waittask(task, "poweroff vm")
    elif action == "on":
        logger.info("start off vm")
        task = vm_obj.PowerOnVM_Task()
        waittask(task, "poweron vm")


def _clone_vm(
        content, template, vm_name, datacenter_name, vm_folder, datastore_name,
        cluster_name, resource_pool, power_on):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    """

    # if none git the first one
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = get_obj(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    if datastore_name:
        datastore = get_obj(content, [vim.Datastore], datastore_name)
    else:
        datastore = get_obj(
            content, [vim.Datastore], template.datastore[0].info.name)

    # if None, get the first one
    cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)

    if resource_pool:
        resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
    else:
        resource_pool = cluster.resourcePool

    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on

    spec = vim.vm.ConfigSpec()

    dev_changes = []
    for device in template.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualE1000) or isinstance(device, vim.vm.device.VirtualVmxnet3):
            logger.info("delete vm networkcard %s" % device.deviceInfo.label)
            virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
            virtual_nic_spec.device = device
            dev_changes.append(virtual_nic_spec)

    spec.deviceChange = dev_changes
    clonespec.config = spec
    logger.info("cloning VM to new_vm:%s ..." % vm_name)
    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    return task


def clone(template_name, vm_name, content, datacenter_name, datastore, cluster):
    """
        clone template
    :param host:
    :param username:
    :param password:
    :param template_name:
    :param vm_name:
    :return:
    """
    try:
        logger.info("start real clone %s" % template_name)
        poweron = False
        template = get_obj(content, [vim.VirtualMachine], template_name)
        if template:
            vm_state = check_vm_status(template)
            logger.info("get tpl obj success")
            task = _clone_vm(content, template, vm_name, datacenter_name, "", datastore, cluster, "", poweron)
            time.sleep(2)
            waittask(task, "wait clone task")
            logger.info("clone %s is complete task status is %s" % (vm_name, task.info.state))
            has_tpl = get_obj(content, [vim.VirtualMachine], vm_name)
            if has_tpl:
                logger.info("task success and vm:%s found in vcenter" % vm_name)
                if vm_state:
                    op_vm(vm_obj=template, action="on")
                return 1
            else:
                logger.info("task success and vm:%s not found in vcenter" % vm_name)
                return 0
        else:
            return 0
    except Exception as e:
        logger.info("clone when catch error:%s" % traceback.format_exc())
        return -1


def delete_vm_networkcard(vm_name, content):
    try:
        vm_obj = get_obj(content, [vim.VirtualMachine], vm_name)
        logger.info("start delete vm:%s networkcard" % vm_name)
        for device in vm_obj.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualE1000) or isinstance(device, vim.vm.device.VirtualVmxnet3):
                logger.info("delete vm networkcard %s" % device.deviceInfo.label)
                virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
                virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                virtual_nic_spec.device = device
                dev_changes = []
                dev_changes.append(virtual_nic_spec)
                spec = vim.vm.ConfigSpec()
                spec.deviceChange = dev_changes
                task = vm_obj.ReconfigVM_Task(spec=spec)
                waittask(task, "delete vm networkcard")
        return 1
    except Exception as e:
        return -1


def vm_to_template(vm_name, template_name, host, username, password, datacenter_name, datastore, cluster):
    logger.info("start make vm:%s to template:%s" % (vm_name, template_name))
    si = connect_vcenter(host=host, username=username, password=password)
    content = si.content
    logger.info("si contnet is %s" % si)
    # 对于 clone 来说 原先的 vm_name 应该作为模板
    has_clone = clone(template_name=vm_name, vm_name=template_name, content=content, datacenter_name=datacenter_name,
                      datastore=datastore, cluster=cluster)
    if has_clone == 1:
        if si:
            logger.info("delete vcenter connect")
            sock = si._stub.pool[0][0]._wrapped.sock
            sock.close()
        return 1
    else:
        if si:
            logger.info("delete vcenter connect")
            sock = si._stub.pool[0][0]._wrapped.sock
            sock.close()
        return -1


def add_template(template_name, params):
    """
        调用接口增加 tenplate_name
    :param template_name:
    :param customer_id:
    :return:
    """
    logger.info("start post tpl:%s to core" % template_name)

    params["name"] = template_name
    params["template_type"] = 'private'
    params["vmware_tool"] = True
    params["product_type"] = ""
    params["template_id"] = str(uuid.uuid4())

    try:
        resp = requests.post(settings.CORE_API, json=params)
        result = json.loads(resp.content)
        logger.info("tpl json is %s" % result)
        template_id = result.get("template_id", None)
        return str(template_id)
    except Exception:
        return None


def filter_stat_data(data, filter_type):
    """
        通过不同类型返回不同的数组
    :param data:
    :param filter_type:
    :return:
    """
    filter_data = []

    if filter_type == "hours":
        # 对于一天之内的需要
        interval = len(data) / 4
        filter_data.append(round(float(data[0]), 2))
        filter_data.append(round(float(data[interval]), 2))
        filter_data.append(round(float(data[interval + interval]), 2))
        filter_data.append(round(float(data[interval * 3]), 2))
        filter_data.append(round(float(data[-1]), 2))
        logger.info(filter_data)
        return filter_data
    else:
        # 只返回天的情况
        start = 0
        filter_data.append(round(float(data[0]), 2))
        interval = len(data) / 8
        for i in range(8):
            start += interval
            filter_data.append(round(float(data[start]), 2))
        filter_data.append(round(float(data[-1]), 2))
        return filter_data


def datastore_info(host, username, password, datastore):
    """
        存储卷的信息
    :param host:
    :param username:
    :param password:
    :param datastore:
    :return:
    """
    si = connect_vcenter(host=host, username=username, password=password)
    content = si.content
    datastore_obj = get_obj(content, [vim.Datastore], datastore)

    capacity = datastore_obj.summary.capacity / 1024 / 1024 / 1024

    free_space = datastore_obj.info.freeSpace / 1024 / 1024 / 1024

    return capacity, free_space


def destroy_tpl(host, username, password, tpl_name):
    """
        删除 模板
    """
    try:
        si = connect_vcenter(host=host, username=username, password=password)
        content = si.content
        tpl_obj = get_obj(content, [vim.VirtualMachine], tpl_name)
        destroy(tpl_obj=tpl_obj)
        return True, "success"
    except Exception as e:
        logger.info("destroy tpl when catch error:%s" % str(e))
        return False, str(e)


def destroy(tpl_obj):
    """
        销毁 模板的 虚拟机
    """
    delete = tpl_obj.Destroy()
    waittask(delete, "vm delete task is doing")
    logger.info("delete tpl_task is doing")

