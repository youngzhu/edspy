__version__ = "0.1.0"
__author__ = "youngzy"


from pathlib import Path
import sys

import logging.config

# 这俩没区别啊，都可以
# src_root = Path(__file__).parent.parent
src_root = Path(__file__).parent
sys.path.append(str(src_root))


# 日志
log_config = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
            "level": "INFO",
            "encoding": "utf-8"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    }
}

logging.config.dictConfig(log_config)
_logger = logging.getLogger(__name__)

# 暴露记录器供外部使用
# 没有也不影响使用啊
# __all__ = ["logger"]