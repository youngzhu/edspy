from edspy.mimi import Mimi
from edspy.settings import Settings

class EdsReportor:
    def __init__(self) -> None:
        self.mimi = Mimi()
        self.settings = Settings()