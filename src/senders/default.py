# -*- coding: utf-8 -*-
import logging
import urllib
import urllib2
from datetime import datetime


last_hour = datetime.now().strftime('%H')
last_hour_send_count = 0


class Sender(object):
    'Sender插件类，必须使用Sender作为类名'

     
    def __init__(self, options):
        '插件初始化方法，options是插件配置数据'
        self.options = options
        self.url = 'https://warnings.sinaapp.com/send_warning/' + options['user_id']

    def send(self, title, content, level=0, cate='default', host='default', appname='default'):
        '插件方法，必须实现'
        try:
            data = locals()
            data['app_id'] = self.options['app_id']
            del data['self']
            data = urllib.urlencode(data)

            global last_hour, last_hour_send_count
            this_hour = datetime.now().strftime('%H')
            logging.info('begin sender.default send:%s %s %s', title, self.url, data)

            # 每小时最大报警次数
            one_hour_max_send = int(self.options['one_hour_max_send'])
            if one_hour_max_send > 10: # 防止无节操报警
                one_hour_max_send = 10
            if this_hour == last_hour and last_hour_send_count >= one_hour_max_send:
                logging.info('sender.default not send one_hour_max_send :%s %s %s', title, data, last_hour_send_count)
                return

            # 设置最后一次报警的小时
            if this_hour != last_hour:
                last_hour = this_hour
                last_hour_send_count = 0
           
            # 设置最后一个小时已经发送的报警次数
            last_hour_send_count = last_hour_send_count + 1

            rsp = urllib2.urlopen(self.url, data)
            logging.info('end sender.default send to :%s %s %s', title, self.url, rsp.read())
        except urllib2.HTTPError, he:
            logging.info('sender.default send error:%s %s %s', level, title, he.code)
        except urllib2.URLError, ue:
            logging.info('sender.default send error:%s %s %s', level, title, ue.reason)
        except Exception:
            logging.exception('sender.default send error:%s %s', level, title)
