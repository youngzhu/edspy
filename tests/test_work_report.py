from edspy.work_report import get_work_report

import re

def test_get_work_report_by_llm(eds_reportor):
    """测试通过大语言模型生成的周报"""
    work_report = get_work_report(eds_reportor)
    assert work_report is not None
    assert len(work_report.work_plan) > 0

def test_get_work_report_from_file():
    """测试从本地文件获取周报"""
    work_report = get_work_report(eds_reportor=None)
    assert work_report is not None
    assert len(work_report.work_plan) > 0 

from datetime import date

def test_file_name():
        file_name = f"work-report-{date.today()}.json"
        pattern = re.compile(r"work-report-\d{4}-\d{2}-\d{2}.json")
        assert pattern.match(file_name)


class TestWorkReport:
    def test_work_plans(self, work_report_local):
        """测试字符串形式的工作计划"""
        work_plans = work_report_local.work_plans()

        pattern = r"1\. .*\n2\. .*"
        # assert '\n' in work_report.work_plans()
        assert re.match(pattern, work_plans), f"工作计划 '{work_plans}' 不符合模式 '1. xxx\\n2. xxx'"

    def test_daily_work_report(self, work_report_local):
        """测试获取日报内容函数"""
        daily = work_report_local.daily_work_report()
        assert daily in work_report_local.work_plan