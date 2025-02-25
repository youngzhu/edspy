import os

# class Secrets: # 名字与标准库中的重复了
class Mimi:
    """不能说的秘密"""
    def __init__(self) -> None:
        self.open_ai_api_key = os.getenv('OPEN_AI_API_KEY')
        self.open_ai_base_url = os.getenv('OPEN_AI_BASE_URL')
        self.open_ai_model = os.getenv('OPEN_AI_MODEL')