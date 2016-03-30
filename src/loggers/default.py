# -*- coding: utf-8 -*-
import logging
import logging.handlers
import json
from datetime import datetime

from log_watcher import LogWatcher


class Logger(object):
    'Logger插件类，必须使用Logger作为类名'

    log_caches = []

    def __init__(self, options):
        '插件初始化方法，options是插件配置数据'
        self.log_filename = options['log_filename']
        self.max_log_cache = int(options['max_log_cache'])

        my_logger = logging.getLogger('counter')
        my_logger.propagate = False
        my_logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(self.log_filename, maxBytes=100 * 1000 * 1000, backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        handler.setFormatter(formatter)
        my_logger.addHandler(handler)
        self.logger = my_logger

    def log(self, counter_data):
        '插件方法，保存日志数据'
        self.logger.info(json.dumps(counter_data))
        if len(self.log_caches) >= self.max_log_cache:
            self.log_caches.pop(0)

        counter_data['time'] = datetime.now()
        self.log_caches.append(counter_data)

    def get_last_historys(self):
        '所有logger必须实现，返回最近几条计数器日志，用于在报警判断逻辑中使用'
        return self.log_caches

    def readlog_from_file(self, n=10):
        '从日志里读取计数器信息'
        lines = LogWatcher.tail(self.log_filename, 10)
        results = []
        for line in lines:
            if line.find('{') == -1:
                continue
            pos = line.index('{')
            result = json.loads(line[pos:])
            results.append(result)
        return results


if __name__ == '__main__':
    logger = Logger()
    results = logger.readlog_from_file()
    import pprint
    pprint.pprint(results)
