# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

sender = '2629970454@qq.com'
passwd = 'qalexanbaqvnebcc'
receivers = 'gexiaoming@qutoutiao.net,jiaocan@qutoutiao.net,jiaozhigang@qutoutiao.net,liuxinglv@qutoutiao.net'  #'2629970454@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
#receivers = '2629970454@qq.com'
# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("UI自动化", 'utf-8')
message['To'] = Header(receivers, 'utf-8')
subject = 'Python SMTP 邮件测试报告'
message['Subject'] = Header(subject, 'utf-8')

# 邮件正文内容
message.attach(MIMEText('这是Python 邮件发送测试报告……', 'plain', 'utf-8'))

# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('C:\\study\\20200821\\20200821\\20200812\\catlog\\templates\\catlogs.html', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="test_report.html"'
message.attach(att1)

# 构造附件2，传送当前目录下的 runoob.txt 文件
'''att2 = MIMEText(open('ugc.xlsx', 'rb').read(), 'base64', 'utf-8')
att2["Content-Type"] = 'application/octet-stream'
att2["Content-Disposition"] = 'attachment; filename="ugc.xlsx"'
message.attach(att2)'''

try:
    #smtpObj = smtplib.SMTP('smtp.exmail.qq.com', 587)
    smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)
    #smtpObj.starttls()
    smtpObj.login(sender,passwd)
    smtpObj.sendmail(sender, receivers.split(','), message.as_string())
    smtpObj.close()
    print ("邮件发送成功")
except smtplib.SMTPException:
    print ("Error: 无法发送邮件")
