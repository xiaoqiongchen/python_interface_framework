import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

import  Config.ProjConfigVar
def send_mail(attach_file_path):
    mail_host = Config.ProjConfigVar.mail_host  # 设置服务器
    mail_user = Config.ProjConfigVar.mail_user  # 用户名
    mail_pass = Config.ProjConfigVar.mail_pass # 口令
    sender = Config.ProjConfigVar.sender
    receivers = Config.ProjConfigVar.receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = formataddr(["光荣之路吴老师", "testman1980@126.com"])
    message['To'] = ','.join(receivers)
    subject = '自动化测试执行报告'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('最新执行的自动化测试报告，请参阅附件内容！', 'plain', 'utf-8'))

    # 构造附件1，传送测试结果的excel文件
    print(os.path.exists(attach_file_path))
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(open(attach_file_path, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "接口测试报告.HTML"))
    encoders.encode_base64(att)
    message.attach(att)

    try:
        smtpObj = smtplib.SMTP(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)

if  __name__ =="__main__":
    print(Config.ProjConfigVar.test_data_file)
    send_mail(Config.ProjConfigVar.test_data_file)