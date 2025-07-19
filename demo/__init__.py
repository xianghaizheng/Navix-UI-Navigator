# Navix newdemo - 系统化示例包
# 包含从基础到高级的 Navix 功能演示
import sys
from pathlib import Path

def setup_project_path():
    """Ensure the project root is in sys.path for module imports"""
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

setup_project_path()
