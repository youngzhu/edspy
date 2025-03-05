from pathlib import Path
import sys

# 这俩没区别啊，都可以
# src_root = Path(__file__).parent.parent
src_root = Path(__file__).parent
sys.path.append(str(src_root))