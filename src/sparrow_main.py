# -*= coding: utf-8 -*-

from time import sleep
import logging
import sys
import config

logging.basicConfig(level=logging.DEBUG)

def log_uncaught_exceptions(ex_cls, ex, tb):
    '对未处理异常记录日志'
    import traceback
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_cls, ex))

sys.excepthook = log_uncaught_exceptions


def send_warning(data):
    for sender in config.warning_senders:
        try:
            sender.send(**data)
        except:
            logging.exception('send_warning(error:%s', sender.__module__)


def counter_handler(data):
    '遍历每一个报警规则来处理当前计数值'
    for rule in config.warning_rules:
        try:
            historys = config.counter_logger.get_last_historys()
            result = rule.process(data, historys)
            if result:
                send_warning(result)
        except:
            logging.exception('counter_handler error:%s', rule.__module__)


def get_counter_data():
    '获取每个计数器最新值'
    result = {}
    for counter in config.warning_counters:
        try:
            data = counter.get_data()
            result.update(data)
        except:
            logging.exception('get_counter_dataerror:%s', counter.__module__)
    return result


def main():
    while True:
        try:
            # get the data
            data = get_counter_data()
            logging.debug('gen_counter:%s', data)
            # add the date into data
            config.counter_logger.log(data)
            # handler the data
            counter_handler(data)
        except KeyboardInterrupt:
            raise
        except:
            logging.exception('main error')
        finally: # 防止出错时死循环
            sleep(config.logger_interval)

if __name__ == '__main__':
    main()
