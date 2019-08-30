import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendEmailFJ:
    def __init__(self,repaort_name=''):
        if repaort_name:
            self.report_name =repaort_name
        else:
            self.report_name = "自动化测试报告"
        self.sender = 'jinxuedieww@163.com'
        self.receiver = '270002181@qq.com'
        self.smtpserver = 'smtp.163.com'
        self.username = 'jinxuedieww@163.com'
        self.password = '143812ww'
        self.mail_title = '{}'.format(self.report_name)

    def send_email_fj(self,sub_report_name,file_name,success_count,fail_count,all_count):
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receiver
        message['Subject'] = Header(self.mail_title, 'utf-8')
        if all_count >0:
            success_percet = str((success_count/all_count)*100)+"%"
        else:
            success_percet = "0%"
        # 邮件正文内容
        message.attach(MIMEText('以下是<{}>自动化测试报告,一共执行<{}>条测试用例，其中通过<{}>条，通过率<{}>,详情请查看附件测试报告'.format(sub_report_name,all_count,success_count,success_percet), 'plain', 'utf-8'))

        # 构造附件1（附件为html格式的文本）
        att1 = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename={}'.format(file_name)
        message.attach(att1)

        # # 构造附件2（附件为JPG格式的图片）
        # att2 = MIMEText(open('123.jpg', 'rb').read(), 'base64', 'utf-8')
        # att2["Content-Type"] = 'application/octet-stream'
        # att2["Content-Disposition"] = 'attachment; filename="123.jpg"'
        # message.attach(att2)
        #
        # # 构造附件3（附件为HTML格式的网页）
        # att3 = MIMEText(open('report_test.html', 'rb').read(), 'base64', 'utf-8')
        # att3["Content-Type"] = 'application/octet-stream'
        # att3["Content-Disposition"] = 'attachment; filename="report_test.html"'
        # message.attach(att3)

        smtpObj = smtplib.SMTP_SSL()  # 注意：如果遇到发送失败的情况（提示远程主机拒接连接），这里要使用SMTP_SSL方法
        smtpObj.connect(self.smtpserver)
        smtpObj.login(self.username, self.password)
        smtpObj.sendmail(self.sender, self.receiver, message.as_string())
        print("邮件发送成功！！！")
        smtpObj.quit()

if __name__ == "__main__":
    filename = "/Users/majing/Downloads/home/ma/桌面/InterfaceTest/python_excel/hz_file/7.html"
    smfj = SendEmailFJ("测试发送邮件")
    smfj.send_email_fj("测试发送邮件功能",filename,1,99,100)