import pytest
import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
src_root = Path(__file__).parent.parent
sys.path.append(str(src_root))

from eds_logger import EdsLogger

@pytest.fixture
def eds_logger():
    return EdsLogger()