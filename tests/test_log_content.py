import sys
import os
from pathlib import Path
from datetime import date
import re

from eds_logger import EdsLogger

## conftest 中处理了，这里可以省略
# 将项目根目录添加到 sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# src_root = Path(__file__).parent.parent
# sys.path.append(str(src_root))

from log_content import LogContent

class TestLogContent:

    def test_default(self, eds_logger):
        """测试从本地读取数据"""
        logContent = LogContent(eds_logger)
        logContent._default()
        assert len(logContent.dailyWorkContent) > 0
        assert logContent.weeklyPlanStudy

    def test_file_name(self):
        file_name = f"log-content-{date.today()}.json"
        file_pattern = re.compile(r"log-content-\d{4}-\d{2}-\d{2}.json")
        assert file_pattern.search(file_name)