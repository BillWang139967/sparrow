## Sparrow

### 简单介绍###

麻雀虽小、五脏俱全

Sparrow用来定时收集你服务器运行状态、性能、业务等信息，根据你定义好的规则，发现异常后通知你。

Sparrow定位是一个很简单就能安装使用的本机监控软件，不需要运营一个网站，
而且强调扩展性，让人们去开发各种插件满足不同的监控需求以及和自己的监控系统集成。

### 快速上手

下载安装

    cd Sparrow/src

打开config.ini，修改报警邮件配置

    [sender:mail]
    name = mail 
    smtphost = smtp.163.com
    username = sendwarnings@163.com
    password = password
    from = sendwarnings@163.com
    ;可以用逗号隔开写多个报警收件人
    to = wawasoft@qq.com
    ssl = False
    ;每小时最多发送多少报警
    one_hour_max_send = 1

配置主机的基本报警规则

    [rule:default]
    name = default
    ;主机名，对外发送报警时，区分多台机器
    host = wawahost
    ;以下每行为一个报警规则，格式为"计数器名称 阈值 超过阈值最大次数 报警的标题"
    rule1 = cpu_utilization 70 5 CPU使用率连续5次超过70%
    rule2 = mem_utilization 70 5 内存使用率连续5次超过70%
    rule3 = swap_utilization 70 5 交换分区使用率连续5次超过70%
    rule4 = disk_utilization 70 5 磁盘使用率连续5次超过70%

如果要确保本机必须监听某些端口，做如下配置

    [rule:tcpport]
    name = tcpport 
    host = wawahost
    ;格式为"ip port 报警的标题"
    rule1 = 127.0.0.1 80 nginx端口挂掉
    rule2 = 127.0.0.1 27017 mongodb端口挂掉
    rule3 = 127.0.0.1 3306 mysql端口挂掉

如果要确保本机必须运行某些进程，做如下配置

    [rule:process]
    name = process 
    host = wawahost
    ;格式为"进程cmdline的正则匹配模式 报警的标题", 报警标题为最后一个空格之后的文字
    rule1 = gunicorn mainweb:wsgiapp.*-k gevent 检测到wsgiapp进程不存在

运行

    python Sparrow_main.py

可以睡个好觉了，服务有问题你会收到通知的。

小技巧

1. 最好专门申请一个独立的邮箱用来发送报警，163,qq都可以免费注册邮箱。
1. 接收报警的邮箱推荐用qq邮箱，引起如果你开通了微信的话，收到邮件后手机会有提醒。

