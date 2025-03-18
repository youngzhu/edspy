from edspy.work_report import get_work_report

def test_get_work_report_by_llm(eds_reportor):
    work_report = get_work_report(eds_reportor)
    assert work_report is not None
    assert len(work_report.work_plan) > 0