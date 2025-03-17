__version__ = "0.1.0"
__author__ = "youngzy"


from pathlib import Path
import sys

# 这俩没区别啊，都可以
# src_root = Path(__file__).parent.parent
src_root = Path(__file__).parent
sys.path.append(str(src_root))


# 日志
import logging.config
import yaml

with open("logging_config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)
logging.config.dictConfig(config)
_logger = logging.getLogger(__name__)

# 暴露记录器供外部使用
# 没有也不影响使用啊
# __all__ = ["logger"]