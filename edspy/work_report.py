"""提供周报和日报的内容

主要有完成以下任务：
1. 通过大语言模型生成内容
2. 生成新的JSON文件，以备当LLM服务不可用时，取本地数据
"""
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from random import choice

@dataclass_json
@dataclass(frozen=True)
class WorkReport:
    # 为了符合Python、JSON的规范，如此命名
    # 上周工作任务完成情况
    last_week_work_content: str = field(
        metadata=config(field_name="lastWeekWorkContent")  # 指定 JSON 中的键名
    )
    # 上周学习完成任务情况
    last_week_study_content: str = field(
        metadata=config(field_name="lastWeekStudyContent")
    )
    # 经验和收获总结
    last_week_summary: str = field(
        metadata=config(field_name="lastWeekSummary")
    ) 
    # 本周工作计划与重点
    work_plan: list[str] = field(
        metadata=config(field_name="workPlan")
    ) 
    # 本周学习计划
    study_plan: str = field(
        metadata=config(field_name="studyPlan")
    ) 

    def work_plans(self):
        """以文本形式返回本周工作计划
        学某些函数，s代表str
        
        返回类似：
        1. Task 1
        2. Task 2
        3. Task 3
        """
        # return '\n'.join(self.work_plan)
        # result = ''
        # for i, plan in enumerate(self.work_plan):
        #     result += f"{str(i+1)}. {plan}\n"
        result = "\n".join(f"{i+1}. {plan}" for i, plan in enumerate(self.work_plan))

        return result

    def daily_work_report(self):
        """获取日报内容
        从工作计划中随机取一条"""
        return choice(self.work_plan)

    def check(self):
        """检查生成的内容。
        如果规则都满足，则返回 True
        否则，返回 False
        """
        # 工作计划列表长度应该在 3-5
        if not (3 <= len(self.work_plan) <= 5):
            return False

        return True



from . import _logger
import time

def get_work_report(eds_reportor):
    """获取周报内容对象
    首先调AI大语言模型来生成内容
    如果失败则从本地获取
    """
    try:
        _logger.info("AI生成 start...")
        start = time.perf_counter()
        work_report = _complete(eds_reportor)
        elapsed = time.perf_counter() - start
        _logger.info(f"AI生成 end. 耗时 {elapsed:0.3f}s")
    except Exception as e:
        _logger.error(f"调用大语言模型发生错误：{e}")
        work_report = _load_from_file()
    else:
        # 更新本地数据
        _write_to_file(work_report)

    return work_report

from openai import OpenAI

def _complete(eds_reportor):
    """调大语言模型生成内容"""
    prompt = f"""
    我是个后端开发人员，开发语言以Java为主，目前参与开发的是寿险营运一站式服务平台，负责保全退保模块。
    不要出现重构、优化等字眼，还在学习。
    数据库用的少，不要提到数据库。
    请以JSON格式返回一个周报。
    要求：
    1. 不要出现具体的周几或星期几
    2. 3-5 表示一个随机的数值范围 [3, 5]
    3. 不要出现JDK的版本
    4. 不要出现技术分享会
    
    包含以下内容（其中多项不需要列表，要有序号，用换行符分割）：
    1. 上周工作任务完成情况（lastWeekWorkContent）：3-5条内容
    2. 上周学习完成任务情况（lastWeekStudyContent）：3-5项
    3. 经验和收获总结（lastWeekSummary）
    4. 本周学习计划（studyPlan）：1-2项
    5. 本周工作计划与重点（workPlan）：以列表形式返回3-5项，不要序号
    """

    client = OpenAI(
        api_key=eds_reportor.mimi.open_ai_api_key, 
        base_url=eds_reportor.mimi.open_ai_base_url
    )

    retries = 3 # 多尝试几次，还是不行则抛异常
    for i in range(retries):
        response = client.chat.completions.create(
            model=eds_reportor.mimi.open_ai_model,
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
        result = WorkReport.from_json(cleaned_json)
        if result.check():
            break
        else:
            _logger.error('生成的数据不合规')

        if i == retries - 1:
            raise ValueError(f'尝试了{retries}次，生成的内容还是不合规')

    return result 


from pathlib import Path
DATA_DIR = Path(__file__).parent.parent / "data"

import re

def _load_from_file():
    """从本地文件中读取"""
    start_with = re.compile(r'^work-report.*')  # 匹配以 work-report 开头的文件名
    files = [file for file in DATA_DIR.iterdir() if start_with.match(file.name) and file.is_file()]
    random_file = choice(files)
    _logger.info(f"读取的本地文件：{random_file.name}")

    # 读取文件
    json_data = random_file.read_text(encoding="utf-8")
    return WorkReport.from_json(json_data)

from datetime import date

def _write_to_file(work_report):
    """将大语言模型生成的内容存入本地"""
    file_name = f"work-report-{str(date.today())}.json"
    json_file = DATA_DIR / file_name
    json_file.write_text(
        work_report.to_json(ensure_ascii=False, indent=4), 
        encoding='utf-8',
    )