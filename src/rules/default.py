# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

RuleConfig = namedtuple('RuleConfig', ['counter_name', 'max_value', 'max_count', 'title'])


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
            # 计数器不存在直接跳过
            max_value = float(rule.max_value)
            max_count = int(rule.max_count)
            if rule.counter_name not in data:
                continue
            # 当前计数器值没有到达阈值直接跳过
            if float(data[rule.counter_name]) < max_value:
                continue

            this_historys = historys[-max_count:]
            # 计数器历史不足时直接跳过
            if len(this_historys) < max_count:
                continue

            this_historys = [float(history[rule.counter_name]) for history in this_historys]
            # 最近几次的计数器值如果有小于阈值的则直接跳过
            if any([h < max_value for h in this_historys]):
                continue
           
            logging.debug('will raise warning:%s %s', rule, this_historys)
            return self._get_send_data(rule, data, historys)

        return None  # 返回None不需报警

    def _get_send_data(self, rule, data, historys):
        result = {}
        result['title'] = rule.title
        result['content'] = str([(h['time'].strftime('%Y-%m-%d %H:%M:%S'), h[rule.counter_name])
                                 for h in historys[-int(rule.max_count):]])
        result['host'] = self.options['host'] if 'host' in self.options else 'default'
        return result
