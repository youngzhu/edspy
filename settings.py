import os

class Settings:
    """配置信息，如URL等
    
    urls:
  home: http://eds.newtouch.cn
  login: 
  daily: 
  weekly: http://eds.newtouch.cn/eds36web/WorkWeekly/WorkWeeklyInfo.aspx
host: eds.newtouch.cn
hplb:
  workType: 开发-计划阶段
  action: ""
    """
    def __init__(self) -> None:
        self.login_url = "http://eds.newtouch.cn/eds3/login.html"
        self.daily_url = "http://eds.newtouch.cn/eds3/worklog.aspx?tabid=0"

        self.debugging = os.getenv("DEBUGGING")
        self.action = os.getenv("ACTION")