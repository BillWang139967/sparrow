# -*- coding: utf-8 -*-
#import psutil
import si


def get_sysinfo():
    result = {}
    # result['cpu_utilization'] = psutil.cpu_percent()
    meminfo = si.Server.meminfo()
    result['mem_utilization'] = meminfo['mem_used_rate']
    result['swap_utilization'] = meminfo['swap_used_rate']
    
    mounts = si.Server.mounts(True)
    for mount in mounts:
        result['disk_utilization(%s)' % mount['path']] = mount['used_rate']
    return result


class Counter(object):
    'Counter插件类，必须使用Counter作为类名'
    
    def __init__(self, options):
        '插件初始化方法，options是插件配置数据'
        self.options = options

    def get_data(self):
        '插件专用方法，必须返回一个字典'
        return get_sysinfo()


if __name__ == '__main__':
    import pprint
    pprint.pprint(get_sysinfo())
