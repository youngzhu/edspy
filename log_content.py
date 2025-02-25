from pathlib import Path
import json

class LogContent:
    """提供周报和日报的内容

    主要有完成以下任务：
    1. 通过大语言模型生成内容
    2. 替换原有的本地文件，以备当LLM服务不可用时，取本地数据
    """

    def __init__(self) -> None:
        # 每日工作内容，列表，使用时随机取一条
        # self.dailyWorkContent = []
        # weeklyWorkContent # 本周工作内容,
        # weeklyStudyContent # 本周学习计划,
        # weeklySummary # 本周总结,
        # weeklyPlanWork # 下周工作计划,
        # weeklyPlanStudy # 下周学习计划
        pass
        

    def get(self):
        """调大语言模型生成内容，如果失败则从本地获取"""
        try:
            self._complete()
        except Exception:
            self._default()

    def _complete(self):
        """调大语言模型生成内容"""
        raise Exception("暂未实现")

    # 默认返回本地文件中的数据
    def _default(self):
        """默认读取本地文件中的数据返回"""
        # 测试无法通过
        # path = Path('data/log-content.json')
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "log-content.json"

        # 读取文件
        with open(data_path, "r", encoding="utf-8") as f:
            jsonContent = json.load(f)

        # print(jsonContent)
        self._from_json(jsonContent)
    
    def _from_json(self, jsonContent):
        """根据JSON串设置属性"""
        # 每日工作内容,
        self.dailyWorkContent = jsonContent['dailyWorkContent']
        # 本周工作内容,
        self.weeklyWorkContent = jsonContent['weeklyWorkContent']
        # 本周学习计划,
        self.weeklyStudyContent = jsonContent['weeklyStudyContent']
        # 本周总结,
        self.weeklySummary = jsonContent['weeklySummary']
        # 下周工作计划,
        self.weeklyPlanWork = jsonContent['weeklyPlanWork']
        # 下周学习计划
        self.weeklyPlanStudy = jsonContent['weeklyPlanStudy']
