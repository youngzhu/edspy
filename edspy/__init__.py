__version__ = "0.1.0"
__author__ = "youngzy"

from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import sys

# 这俩没区别啊，都可以
# src_root = Path(__file__).parent.parent
src_root = Path(__file__).parent
sys.path.append(str(src_root))


# 日志
import logging.config
import yaml

# 获取项目根目录（假设配置文件在根目录下）
PROJECT_ROOT = Path(__file__).parent.parent
config_path = PROJECT_ROOT / "logging_config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
logging.config.dictConfig(config)
_logger = logging.getLogger(__name__)

# 暴露记录器供外部使用
# 没有也不影响使用啊
# __all__ = ["logger"]