from edspy.eds_reportor import EdsReportor

class TestEdsReportor:
    def test_weekly_report_map(self, work_report_local):
        """验证周报页面元素和WorkReport的映射关系是否能获取到正确的值"""
        list = []
        for key, val in EdsReportor.WEEKLY_REPORT_MAP.items():
            list.append(f"{key}: {getattr(work_report_local, val)}\n")

        # assert len(list) == len()
