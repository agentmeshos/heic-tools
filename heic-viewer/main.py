#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HEIC图像查看器 - 主入口
支持查看、转换HEIC格式图像文件
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from gui.main_window import MainWindow


def main():
    """主函数"""
    try:
        # 创建并运行应用
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
        sys.exit(1)


if __name__ == "__main__":
    main()
