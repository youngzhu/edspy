import os

class Settings:
    """配置信息，如URL等
    """
    def __init__(self) -> None:
        self.login_url = "http://eds.newtouch.cn/eds3/login.html"
        self.daily_url = "http://eds.newtouch.cn/eds3/worklog.aspx"
        self.weekly_url = "http://eds.newtouch.cn/eds36web/WorkWeekly/WorkWeeklyInfo.aspx"

        self.debugging = os.getenv("DEBUGGING")
        self.action = os.getenv("ACTION")