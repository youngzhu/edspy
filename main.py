from edspy.eds_reportor import EdsReportor, _logger
from edspy.mail import Mail
from datetime import date


if __name__ == '__main__':
    app = EdsReportor()
    mail = Mail(app)

    today = date.today()

    try:
        app.run()
        # mail.send(f"{today}生成成功", "RT")
    except Exception as e:
        _logger.error(f"异常：{e}")
        _logger.error(f"异常：{e.with_traceback}")
        # mail.send(f"{today}失败", f"错误：\n{str(e)}")
