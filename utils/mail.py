# -coding=utf-8 -*-
import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.config import Config, REPORT_PATH
from utils.log import Logger

logger = Logger(__name__).get()

class Mail:
    def __init__(self, filename=None):
        self.con = Config()
        self.mail_server = self.con.get('mail_server')
        self.user = self.con.get('mail_user')
        self.password = self.con.get('mail_pwd')
        self.sender = self.con.get('sender')
        self.receiver = self.con.get('receiver')
        self.subject = self.con.get('subject')
        self.content = self.con.get('content')
        self.debuglevel = int(self.con.get('debuglevel'))

        # 如果一封邮件中含有附件，那邮件的Content-Type域中必须定义multipart/mixed类型
        # multipart/related类型：将其它内容以内嵌资源的方式存储在邮件中
        self.msg = MIMEMultipart('related')

        self.filename = filename  # list or str
        self.content_id = 0

    # 添加为附件
    def __add_attachment(self, filename):

        file_path = os.path.join(REPORT_PATH, filename)

        with open(file_path, 'rb') as f:
            mb = MIMEBase('application', 'octet-stream')
            # 加上信息头
            mb.add_header('Content-Disposition', 'attachment', filename=filename)
            mb.add_header('Content-ID', '<%d>' % self.content_id)
            self.content_id += 1
            # mb.add_header('X-Attachment=Id', '0')
            # 读取附件内容
            mb.set_payload(f.read())
            # 用base64编码
            encoders.encode_base64(mb)
            # 添加到MIMEMultipart
            self.msg.attach(mb)

        # att = MIMEText(open(file_path, 'rb').read(), 'plain', 'utf-8')
        # att['Content-Type'] = 'application/octet-stream'
        # att['Content-Disposition'] = 'attachment; filename="%s"' % filename
        # self.msg.attach(att)
        logger.info('Attach %s as an attachment success.' % self.filename)

    # 将附件的html直接写入邮件正文
    def __html_to_body(self, file):
        file_path = os.path.join(REPORT_PATH, file)
        with open(file_path, 'rb') as f:
            html = f.read()
            self.msg.attach(MIMEText(html, 'html', 'utf-8'))

    def send(self):
        self.msg['Subject'] = Header(self.subject, 'utf-8')
        self.msg['From'] = Header(self.user)
        self.msg['To'] = Header(self.receiver)

        # 邮件正文是MIMEText
        if self.content:
            text = MIMEText(self.content, 'plain', 'utf-8')
            text.add_header('Content-ID', '<%d>' % self.content_id)
            self.content_id += 1
            self.msg.attach(text)

        # 添加为附件，并写入正文
        try:
            if self.filename:
                if isinstance(self.filename, list):
                    for x in self.filename:
                        self.__add_attachment(x)
                        self.__html_to_body(x)
                elif isinstance(self.filename, str):
                    self.__add_attachment(self.filename)
                    self.__html_to_body(self.filename)
        except FileNotFoundError:
            logger.exception('file not found:'+self.filename, exc_info=True)
            return False

        smtp = smtplib.SMTP()
        try:
            smtp.connect(self.mail_server)
            # debuglevel=1，打印出和SMTP服务器交互的所有信息
            smtp.set_debuglevel(self.debuglevel)
            smtp.login(self.user, self.password)
            smtp.sendmail(self.sender, self.receiver.split(','), self.msg.as_string())
        except smtplib.SMTPException:
            logger.exception('Mail failed to send:', exc_info=True)
        finally:
            smtp.quit()
            logger.info('Mail sent successfully')

        return True

# Mail('20190222175825result.html').send()
