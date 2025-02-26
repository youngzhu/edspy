import os

from dotenv import load_dotenv

from settings import Settings
from log_content import LogContent
from mimi import Mimi

from selenium import webdriver

class EdsLogger:
    def __init__(self):
        load_dotenv()
        self.mimi = Mimi()
        self.settings = Settings()


        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # options.add_argument('--allow-insecure-localhost')  # 允许本地不安全的连接

        # 为什么不能起名为 webdriver ？
        # self.webdriver = webdriver.Chrome()
        self.driver = webdriver.Chrome(options=options)


    def run(self):
        """完成每周的周报和日报"""
        print("Run the logger")
        self._login()

        # 准备周报的数据
        # self._prepped_data()

        # 开始填日报
        # self._do_daily_log()

    def _do_daily_log(self):
        print(f'日报内容：{self.logContent.daily()}')


    def _prepped_data(self):
        """准备周报数据"""
        self.logContent = LogContent(self)
        self.logContent.get()

    
    def _login(self):
        """登录"""
        userId = os.getenv("USER_ID")
        # print("Login as user: " + userId)
        print(self.settings.login_url)
        # self.driver.get(self.settings.login_url)

        