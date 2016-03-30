# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

RuleConfig = namedtuple('RuleConfig', ['host', 'port', 'title'])

import socket

def port_is_open(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        s.close()
        return True
    except:
        return False

class Rule(object):
    'Rule插件类，必须使用Rule作为类名'
     
    def __init__(self, options):
        '插件初始化方法，options是插件配置数据'
        self.options = options
        self._load_rules()

    def _load_rules(self):
        self.rules = []
        for k, v in self.options.items():
            if not k.startswith('rule'):
                continue
            rule = RuleConfig._make(v.split())
            logging.info('load rule config:%s', rule)
            self.rules.append(rule)

    def process(self, data, historys):
        '''插件方法，必须实现
        data是最新的计数数据，caches是最近的数据'''
        logging.debug('rule process:%s', data)
        for rule in self.rules:
            if not port_is_open(rule.host, rule.port):
                return self._get_send_data(rule)

        return None

    def _get_send_data(self, rule):
        result = {}
        result['title'] = rule.title
        result['content'] = '无法连接%s:%s' % (rule.host, rule.port)
        result['host'] = self.options['host'] if 'host' in self.options else 'default'
        return result
