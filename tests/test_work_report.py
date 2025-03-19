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


class TestWorkReport:
    def test_work_plans(self):
        """测试字符串形式的工作计划"""
        work_report = get_work_report(eds_reportor=None)
        work_plans = work_report.work_plans()

        pattern = r"1\. .*\n2\. .*"
        # assert '\n' in work_report.work_plans()
        assert re.match(pattern, work_plans), f"工作计划 '{work_plans}' 不符合模式 '1. xxx\\n2. xxx'"