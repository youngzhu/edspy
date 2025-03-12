from pathlib import Path
import json
from openai import OpenAI
from random import choice
from datetime import date

from . import _logger

DATA_DIR = Path(__file__).parent.parent / "data"

class LogContent:
    """提供周报和日报的内容

    主要有完成以下任务：
    1. 通过大语言模型生成内容
    2. 生成新的JSON文件，以备当LLM服务不可用时，取本地数据
    """

    def __init__(self, eds_logger) -> None:
        # 每日工作内容，列表，使用时随机取一条
        self.mimi = eds_logger.mimi
        

    def get(self):
        """调大语言模型生成内容，如果失败则从本地获取"""
        try:
            _logger.info("AI生成 start...")
            self._complete()
            _logger.info("AI生成 end.")
        except Exception as e:
            print(f"调用大语言模型发生错误：{e}")
            self._default()
        else:
            # 跟新本地数据
            self._save()
        
    def daily(self):
        """从列表中随机取一条作为日报内容"""
        return choice(self.dailyWorkContent)


    def _save(self):
        """将AI生成的内容写入本地"""
        file_name = f"log-content-{str(date.today())}.json"
        json_file = DATA_DIR / file_name
        json_file.write_text(self._jsonContent, encoding='utf-8')

    def _complete(self):
        """调大语言模型生成内容"""
        prompt = f"""
        我是个开发人员，有10年的Java开发工作经验，目前参与开发的是保险业务系统，负责承保和批改模块，和理赔模块无关。
        请以JSON格式返回一个周报。
        包含以下内容（其中多项不需要列表，用换行符分割）：
        1. 每日工作（dailyWorkContent）：以列表形式返回3至5条内容
        2. 每周工作（weeklyWorkContent）：3-5项，要有序号，不要列表
        3. 本周学习计划（weeklyStudyContent）：1-2项
        4. 本周总结（weeklySummary）
        5. 下周工作计划（weeklyPlanWork）：3-5项
        6. 下周学习计划（weeklyPlanStudy）：1-2项
        """

        client = OpenAI(api_key=self.mimi.open_ai_api_key, base_url=self.mimi.open_ai_base_url)

        response = client.chat.completions.create(
            model=self.mimi.open_ai_model,
            messages=[
                # 有或没有，差别不大啊，不清楚这个作用是什么？
                #{"role": "system", "content": "You are a helpful assistant"},
                #{"role": "system", "content": "你是一个KPI完成高手"},
                {"role": "system", "content": "你是一个写报告的小行家"},
                {"role": "user", "content": prompt},
            ],
            temperature=1.5,
            stream=False
        ).choices[0].message.content

        cleaned_json = response.replace('```json', '').replace('```', '').strip()

        # print(cleaned_json)
        # print(f'cleaned_json type: {type(cleaned_json)}')
        self._jsonContent = cleaned_json
        self._from_json(json.loads(cleaned_json))

    def _default(self):
        """默认读取本地文件中的数据"""
        # 测试无法通过
        # path = Path('data/log-content.json')
        # current_dir = Path(__file__).parent
        # data_path = current_dir / "data" / "log-content.json"

        files = [file for file in DATA_DIR.iterdir()]
        random_file = choice(files)
        print(f"读取的本地文件：{random_file.name}")

        # 读取文件
        jsonContent = random_file.read_text(encoding="utf-8")
        # with open(random_file, "r", encoding="utf-8") as f:
        #     jsonContent = json.load(f)

        # print(jsonContent)
        self._from_json(json.loads(jsonContent))
    
    def _from_json(self, jsonContent):
        """根据JSON串设置属性"""
        # <class 'dict'>
        # print(f'jsonContent type: {type(jsonContent)}')
        # 就一行，不好看，不用这个
        # self._jsonContent = json.dumps(jsonContent, ensure_ascii=False)

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

