import os

# class Secrets: # 名字与标准库中的重复了
class Mimi:
    """不能说的秘密"""
    def __init__(self) -> None:
        self.user_id = os.getenv("USER_ID")
        self.user_pwd = os.getenv("USER_PWD")

        self.open_ai_api_key = os.getenv('OPEN_AI_API_KEY')
        self.open_ai_base_url = os.getenv('OPEN_AI_BASE_URL')
        self.open_ai_model = os.getenv('OPEN_AI_MODEL')

        # 发件人和收件人
        self.sender_email = os.getenv("SENDER")
        self.receiver_email = os.getenv("RECEIVER")

        # 发件人的邮箱和密码（或应用专用密码）
        self.smtp_username = os.getenv("SENDER_USERNAME")
        self.smtp_password = os.getenv("SENDER_PASSWD")