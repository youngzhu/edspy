from edspy.eds_logger import EdsLogger
from edspy.mail import Mail
from datetime import date


if __name__ == '__main__':
    app = EdsLogger()
    mail = Mail(app)

    today = date.today()

    try:
        app.run()
        mail.send(f"{today}成功", "RT")
    except Exception as e:
        print(f"异常：{e.with_traceback}")
        mail.send(f"{today}失败", f"错误：\n{str(e)}")
