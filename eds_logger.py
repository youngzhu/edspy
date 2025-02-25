import os

from dotenv import load_dotenv

from settings import Settings
from log_content import LogContent
from mimi import Mimi

class EdsLogger:
    def __init__(self):
        load_dotenv()
        self.mimi = Mimi()
        self.settings = Settings()


    def run(self):
        """完成每周的周报和日报"""
        print("Run the logger")
        self._login()

        # 准备周报的数据
        self._prepped_data()

    def _prepped_data(self):
        """准备周报数据"""
        self.logContent = LogContent(self)
        self.logContent.get()

    
    def _login(self):
        """登录"""
        userId = os.getenv("USER_ID")
        # print("Login as user: " + userId)

        