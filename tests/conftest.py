import pytest
import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#
# 可以，但不推荐
# src_root = Path(__file__).parent.parent
# sys.path.append(str(src_root))

from edspy.eds_logger import EdsLogger
from edspy.eds_reportor import EdsReportor

@pytest.fixture
def eds_logger():
    return EdsLogger()

@pytest.fixture
def eds_reportor():
    return EdsReportor()