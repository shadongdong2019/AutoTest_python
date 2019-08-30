import smtplib
from email.mime.text import MIMEText

class SendEmail:
    global email_server
    global send_user
    global send_psw
    email_server = 'smtp.163.com'
    send_user = 'jinxuedieww@163.com'
    send_psw = '143812ww'

    def  __init__(self):
        pass

    def send_email(self,user_list,sub,content):
        send_user_text = send_user
        message = MIMEText(content,_subtype='plain', _charset='utf-8')
        message['Subject'] = sub
        message['From'] = send_user_text
        message['To'] = ';'.join(user_list)
        server = smtplib.SMTP()
        server.connect(email_server)
        server.login(send_user,send_psw)
        server.sendmail(send_user,user_list,message.as_string())
        server.close()

    def email_main(self,pass_list,fail_list):
        pass_num = float(len(pass_list))
        fail_num = float(len(fail_list))
        total_num = float(pass_num + fail_num)
        pass_percent = float(pass_num/total_num)*100
        content = '一共执行测试用例{}个，通过{}个，通过率为{:.2f}%'.format(total_num,pass_num,pass_percent)
        to_user = ['270002181@qq.com']
        sub = '自动化测试用例邮件'
        self.send_email(to_user,sub,content)

if __name__ == '__main__':
    pass_list = [1,2,5,7]
    fail_list = [3,4,6]
    send_email = SendEmails()
    send_email.email_main(pass_list,fail_list)