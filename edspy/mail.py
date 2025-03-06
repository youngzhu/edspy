import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class Mail():
    def __init__(self, eds_logger) -> None:
        self.mimi = eds_logger.mimi

    def send(self, subject, body):
        """发送邮件"""
        # 创建MIMEMultipart对象
        message = MIMEMultipart()
        message["From"] = self.mimi.sender_email
        message["To"] = self.mimi.receiver_email
        message["Subject"] = subject # 邮件标题

        # 添加邮件正文
        message.attach(MIMEText(body, "plain"))

        # SMTP服务器地址和端口
        smtp_server = "smtp.163.com"
        smtp_port = 25 # TLS 加密 
        # smtp_port = 465 # 使用SSL加密

        # 创建SMTP连接
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            # 使用SSL加密（端口465）
            # server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            # server.set_debuglevel(1)  # 启用调试模式
            server.starttls()  # 启用TLS加密
            server.login(self.mimi.smtp_username, self.mimi.smtp_password)  # 登录邮箱
            text = message.as_string()  # 将邮件内容转换为字符串
            server.sendmail(self.mimi.sender_email, self.mimi.receiver_email, text)  # 发送邮件
            print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败: {e}")
        finally:
            server.quit()  # 关闭SMTP连接