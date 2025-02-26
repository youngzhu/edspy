class Settings:
    """配置信息，如URL等
    
    urls:
  home: http://eds.newtouch.cn
  login: 
  daily: http://eds.newtouch.cn/eds3/worklog.aspx?tabid=0
  weekly: http://eds.newtouch.cn/eds36web/WorkWeekly/WorkWeeklyInfo.aspx
cookie: ASP.NET_SessionId=4khtnz55xiyhbmncrzmzyzzc; ActionSelect=010601; Hm_lvt_416c770ac83a9d996d7b3793f8c4994d=1569767826; Hm_lpvt_416c770ac83a9d996d7b3793f8c4994d=1569767826; PersonId=12234
host: eds.newtouch.cn
hplb:
  workType: 开发-计划阶段
  action: ""
    """
    def __init__(self) -> None:
        self.login_url = "http://eds.newtouch.cn/eds3/login.html"