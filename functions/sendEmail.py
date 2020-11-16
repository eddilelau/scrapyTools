#!/usr/bin/env python
# coding:utf-8
from email.mime.text import MIMEText           #is used to create MIME objects of major type text.
from email.mime.multipart import MIMEMultipart #Creating email and MIME objects from scratch
from email.utils import formataddr            #Miscellaneous utilities
from email.header import Header               #Internationalized headers
import smtplib                                #The smtplib module defines an SMTP client session object that can be used to send mail to any Internet machine with an SMTP or ESMTP listener daemon.

class send_mail(object):
    def __init__(self,my_sender:str,my_pass:str,my_user:str,context:str,my_sender_alias:str,my_user_alias:str):
        self.my_sender = my_sender   # sender email
        self.my_sender_alias = my_sender_alias   # sender email alias
        self.my_pass = my_pass  # 发件人邮箱密码
        self.my_user = my_user  # receiver email
        self.my_user_alias = my_user_alias  # receiver email alias
        self.context = context  # receiver email
        self.message = MIMEMultipart()

    def make_message(self):
        self.message['From'] = Header(self.my_sender_alias, 'utf-8')   # alias the sender email
        self.message['To'] = Header(self.my_user_alias, 'utf-8')      # alias the receiver email
        subject = str(self.context)   # email tittle
        self.message['Subject'] = Header(subject, 'utf-8')
        self.message.attach(MIMEText( str(self.context), 'plain','utf-8'))

    def make_message_with_MIME(self,file_name:str):
        self.message['From'] = Header(self.my_sender_alias, 'utf-8')
        self.message['To'] = Header(self.my_user_alias, 'utf-8')
        subject = str(self.context)
        self.message['Subject'] = Header(subject, 'utf-8')
        self.message.attach(MIMEText( str(self.context), 'plain','utf-8'))

        # add file to MIME
        att1 = MIMEText(open('./zhihu/' + file_name, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', file_name))
        self.message.attach(att1)

    def send_mail(self):
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(self.my_sender, self.my_pass)  # fill password and account
        server.sendmail(self.my_sender, [self.my_user, ], self.message.as_string())  # sender、receiver、content
        return True


if __name__ == '__main__':
    my_sender = '395407702@qq.com'  # 发件人邮箱账号
    my_sender_alias = 'my_sender_alias'  # 发件人邮箱别名
    my_pass = 'frrxawwuwmzybghg'  # 发件人邮箱密码
    my_user = '395407702@qq.com'  # 收件人邮箱账号，我这边发送给自己
    my_user_alias = 'my_user_alias'  # 收件人邮箱账号别名
    context = 'test'
    sd=send_mail(my_sender,my_pass,my_user,context,my_sender_alias=my_sender_alias,my_user_alias=my_user_alias)
    sd.make_message()
    sd.send_mail()
