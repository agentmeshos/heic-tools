"""
工具函数模块
提供文件大小格式化、路径处理等辅助功能
"""
import os
from pathlib import Path
from typing import List, Optional


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小为可读格式

    Args:
        size_bytes: 文件大小(字节)

    Returns:
        格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_size(file_path: str) -> int:
    """
    获取文件大小

    Args:
        file_path: 文件路径

    Returns:
        文件大小(字节)
    """
    try:
        return os.path.getsize(file_path)
    except:
        return 0


def get_heic_files(directory: str, recursive: bool = False) -> List[str]:
    """
    获取目录下的所有HEIC文件

    Args:
        directory: 目录路径
        recursive: 是否递归搜索子目录

    Returns:
        HEIC文件路径列表
    """
    heic_files = []
    extensions = ['.heic', '.heif']

    try:
        if recursive:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if Path(file).suffix.lower() in extensions:
                        heic_files.append(os.path.join(root, file))
        else:
            for item in os.listdir(directory):
                full_path = os.path.join(directory, item)
                if os.path.isfile(full_path) and Path(item).suffix.lower() in extensions:
                    heic_files.append(full_path)
    except Exception as e:
        print(f"扫描目录失败: {e}")

    return sorted(heic_files)


def is_heic_file(file_path: str) -> bool:
    """
    检查文件是否为HEIC格式

    Args:
        file_path: 文件路径

    Returns:
        是否为HEIC文件
    """
    extensions = ['.heic', '.heif']
    return Path(file_path).suffix.lower() in extensions


def ensure_directory(directory: str) -> bool:
    """
    确保目录存在,不存在则创建

    Args:
        directory: 目录路径

    Returns:
        操作是否成功
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


def get_unique_filename(file_path: str) -> str:
    """
    生成唯一的文件名(如果文件已存在,添加数字后缀)

    Args:
        file_path: 原始文件路径

    Returns:
        唯一的文件路径
    """
    if not os.path.exists(file_path):
        return file_path

    path = Path(file_path)
    directory = path.parent
    stem = path.stem
    suffix = path.suffix

    counter = 1
    while True:
        new_path = directory / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return str(new_path)
        counter += 1


def truncate_path(path: str, max_length: int = 50) -> str:
    """
    截断过长的路径用于显示

    Args:
        path: 文件路径
        max_length: 最大长度

    Returns:
        截断后的路径
    """
    if len(path) <= max_length:
        return path

    # 保留开头和结尾
    half = (max_length - 3) // 2
    return f"{path[:half]}...{path[-half:]}"


def validate_output_format(format: str) -> bool:
    """
    验证输出格式是否支持

    Args:
        format: 格式名称

    Returns:
        是否支持
    """
    supported_formats = ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp']
    return format.lower() in supported_formats


# 测试代码
if __name__ == "__main__":
    # 测试文件大小格式化
    print(f"1024 bytes = {format_file_size(1024)}")
    print(f"1048576 bytes = {format_file_size(1048576)}")
    print(f"1073741824 bytes = {format_file_size(1073741824)}")

    # 测试获取HEIC文件
    test_dir = r"d:\7.project\heic-tools\heic-file"
    if os.path.exists(test_dir):
        heic_files = get_heic_files(test_dir)
        print(f"\n找到 {len(heic_files)} 个HEIC文件:")
        for file in heic_files:
            size = get_file_size(file)
            print(f"  {os.path.basename(file)} - {format_file_size(size)}")
