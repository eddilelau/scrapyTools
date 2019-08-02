from email.mime.text import MIMEText           #is used to create MIME objects of major type text.
from email.mime.multipart import MIMEMultipart #Creating email and MIME objects from scratch
from email.utils import formataddr            #Miscellaneous utilities
from email.header import Header               #Internationalized headers
import smtplib                                #The smtplib module defines an SMTP client session object that can be used to send mail to any Internet machine with an SMTP or ESMTP listener daemon.

def send_mail(file_name,kind):
    my_sender = '395407702@qq.com'  # 发件人邮箱账号
    my_pass = 'fxtgbvgdvahubgec'  # 发件人邮箱密码
    my_user = '395407702@qq.com'  # 收件人邮箱账号，我这边发送给自己
    ret = True
    try:
        message = MIMEMultipart()
        message['From'] = Header("知乎搜索结果", 'utf-8')
        message['To'] = Header("工作邮箱", 'utf-8')
        subject = '知乎搜索结果'+'_'+str(kind)
        message['Subject'] = Header(subject, 'utf-8')
        message.attach( MIMEText('知乎搜索结果'+'_'+str(kind) , 'plain', 'utf-8'))      #Add the given payload to the current payload, which must be None or a list of Message objects before the call.


        # 构造附件1，传送当前目录下的 test.txt 文件
        att1 = MIMEText(open('./zhihu/' + file_name, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', file_name))
        # att1["Content-Disposition"] = 'attachment; filename='+file_name
        message.attach(att1)

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print('邮件发送成功')
    except Exception as ex:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print(ex)
        return False