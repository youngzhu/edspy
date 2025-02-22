import os

from dotenv import load_dotenv

class EdsLogger:
    def __init__(self):
        load_dotenv()

    def login(self):
        """登录"""
        userId = os.getenv("USER_ID")
        print("Login as user: " + userId)

    def run(self):
        """完成每周的周报和日志"""
        print("Run the logger")
        self.login()