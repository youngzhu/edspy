import sys
import os
from pathlib import Path

# 将项目根目录添加到 sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
src_root = Path(__file__).parent.parent
sys.path.append(str(src_root))

from log_content import LogContent

class TestLogContent:

    def test_default(self):
        """测试从本地读取数据"""
        logContent = LogContent()
        logContent.get()
        assert len(logContent.dailyWorkContent) > 0
        assert logContent.weeklyPlanStudy