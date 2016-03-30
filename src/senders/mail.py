# -*- coding: utf-8 -*-
import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

last_hour = datetime.now().strftime('%H')
last_hour_send_count = 0

class Sender(object):
    'Sender插件类，必须使用Sender作为类名'
     
    def __init__(self, options):
        '插件初始化方法，options是插件配置数据'
        self.options = options

    def send(self, title, content, level=0, cate='default', host='default', appname='default'):
        try:
            global last_hour, last_hour_send_count
            this_hour = datetime.now().strftime('%H')
            logging.info('begin sender.mail send:%s', title)

            # 每小时最大报警次数
            one_hour_max_send = int(self.options['one_hour_max_send'])
            if one_hour_max_send > 10: # 防止无节操报警
                one_hour_max_send = 10
            if this_hour == last_hour and last_hour_send_count >= one_hour_max_send:
                logging.info('sender.mail not send one_hour_max_send :%s %s', title, last_hour_send_count)
                return

            # 设置最后一次报警的小时
            if this_hour != last_hour:
                last_hour = this_hour
                last_hour_send_count = 0
           
            # 设置最后一个小时已经发送的报警次数
            last_hour_send_count = last_hour_send_count + 1

            msg = MIMEText(content)
            msg['Subject'] = title 
            msg['From'] = self.options['from'] 
            msg['To'] = self.options['to'] 
              
            print self.options
            server = smtplib.SMTP(self.options['smtphost'])  
            if self.options['ssl'] == 'True':
                server.starttls()  
            server.login(self.options['username'],self.options['password'])  
            server.sendmail(self.options['from'], self.options['to'], msg.as_string())
            server.quit()
        except Exception:
            logging.exception('sender.mail send error:%s %s', level, title)
