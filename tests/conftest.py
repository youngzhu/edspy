import pytest
import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#
# 可以，但不推荐
# src_root = Path(__file__).parent.parent
# sys.path.append(str(src_root))

from edspy.eds_reportor import EdsReportor, get_work_report

@pytest.fixture
def eds_reportor():
    return EdsReportor()


@pytest.fixture
def work_report_local():
    """为方便测试，返回一个从本地文件获取内容的 WorkReport 实例"""
    return get_work_report(eds_reportor=None)

@pytest.fixture
def work_report_llm(eds_reportor):
    return get_work_report(eds_reportor=eds_reportor)