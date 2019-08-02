from email.mime.text import MIMEText           #is used to create MIME objects of major type text.
from email.mime.multipart import MIMEMultipart #Creating email and MIME objects from scratch
from email.utils import formataddr            #Miscellaneous utilities
from email.header import Header               #Internationalized headers
import smtplib                                #The smtplib module defines an SMTP client session object that can be used to send mail to any Internet machine with an SMTP or ESMTP listener daemon.

def send_mail(file_name,kind):
    my_sender = '395407702@qq.com'  # �����������˺�
    my_pass = 'fxtgbvgdvahubgec'  # ��������������
    my_user = '395407702@qq.com'  # �ռ��������˺ţ�����߷��͸��Լ�
    ret = True
    try:
        message = MIMEMultipart()
        message['From'] = Header("֪���������", 'utf-8')
        message['To'] = Header("��������", 'utf-8')
        subject = '֪���������'+'_'+str(kind)
        message['Subject'] = Header(subject, 'utf-8')
        message.attach( MIMEText('֪���������'+'_'+str(kind) , 'plain', 'utf-8'))      #Add the given payload to the current payload, which must be None or a list of Message objects before the call.


        # ���츽��1�����͵�ǰĿ¼�µ� test.txt �ļ�
        att1 = MIMEText(open('./zhihu/' + file_name, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # �����filename��������д��дʲô���֣��ʼ�����ʾʲô����
        att1.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', file_name))
        # att1["Content-Disposition"] = 'attachment; filename='+file_name
        message.attach(att1)

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # �����������е�SMTP���������˿���465
        server.login(my_sender, my_pass)  # �����ж�Ӧ���Ƿ����������˺š���������
        server.sendmail(my_sender, [my_user, ], message.as_string())  # �����ж�Ӧ���Ƿ����������˺š��ռ��������˺š������ʼ�
        server.quit()  # �ر�����
        print('�ʼ����ͳɹ�')
    except Exception as ex:  # ��� try �е����û��ִ�У����ִ������� ret=False
        print(ex)
        return False