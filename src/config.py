# -*- coding: utf-8 -*-
import logging
import ConfigParser


cfg = ConfigParser.ConfigParser()
cfg.read('./config.ini')

loglevel = cfg.get('main', 'logging_level')
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, 
                    format='%(asctime)s %(levelname)s %(module)s %(message)s',
                    filename='/var/log/warning-agent.log' if loglevel != 'debug' else None
                    )

logger_interval = cfg.getint('main', 'logger_interval')

warning_rules = []
warning_counters = []
warning_senders = []
counter_logger = None


def init():
    '动态加载各种插件'

    # 动态加载计数器
    options_list = [dict(cfg.items(section)) for section in cfg.sections() if section.startswith('counter:')]
    for options in options_list:
        try:
            name = options['name']
            logging.info('counter init %s', name)
            module = __import__('counters.%s' % name)
            module = getattr(module, name)
            warning_counters.append(module.Counter(options))
        except:
            logging.exception('init counter error:%s', name)

    # 动态加载报警规则
    options_list = [dict(cfg.items(section)) for section in cfg.sections() if section.startswith('rule:')]
    for options in options_list:
        try:
            name = options['name']
            logging.info('rule init %s', name)
            module = __import__('rules.%s' % name)
            module = getattr(module, name)
            warning_rules.append(module.Rule(options))
        except:
            logging.exception('init rule error:%s', name)

    # 动态加载报警发送器
    options_list = [dict(cfg.items(section)) for section in cfg.sections() if section.startswith('sender:')]
    for options in options_list:
        try:
            name = options['name']
            logging.info('sender init %s', name)
            module = __import__('senders.%s' % name)
            module= getattr(module, name)
            warning_senders.append(module.Sender(options))
        except:
            logging.exception('init sender error:%s', name)

    # 动态加载Logger
    logger_name = cfg.get('main', 'logger_name')
    options = dict(cfg.items('logger:%s' % logger_name))
    name = options['name']
    logging.info('logger init %s', name)
    module = __import__('loggers.%s' % name)
    module = getattr(module, name)
    global counter_logger
    counter_logger = module.Logger(options) 


init()

if __name__ == '__main__':
    #print globals()
    print "haha"
    print 
    print  type(warning_rules[0])
    print  warning_counters
    print  warning_senders
    print  type(counter_logger)


