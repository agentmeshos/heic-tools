"""
HEIC文件加载器
负责加载、验证和处理HEIC格式图像文件
"""
import os
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from PIL import Image
from pillow_heif import register_heif_opener
import pillow_heif


class HeicLoader:
    """HEIC文件加载器类"""

    def __init__(self):
        """初始化HEIC加载器并注册HEIF格式支持"""
        self.register_heif_support()
        self._heif_support_registered = True

    @staticmethod
    def register_heif_support():
        """注册HEIF格式支持,使Pillow能够处理HEIC文件"""
        try:
            register_heif_opener()
            return True
        except Exception as e:
            print(f"注册HEIF支持失败: {e}")
            return False

    def validate_heic(self, file_path: str) -> bool:
        """
        验证文件是否为有效的HEIC文件

        Args:
            file_path: 文件路径

        Returns:
            bool: 文件是否有效
        """
        try:
            if not os.path.exists(file_path):
                return False

            # 检查文件扩展名
            ext = Path(file_path).suffix.lower()
            if ext not in ['.heic', '.heif']:
                return False

            # 尝试打开文件验证
            with Image.open(file_path) as img:
                img.verify()

            return True
        except Exception as e:
            print(f"验证HEIC文件失败 {file_path}: {e}")
            return False

    def load_heic(self, file_path: str) -> Optional[Image.Image]:
        """
        加载HEIC文件并返回PIL Image对象

        Args:
            file_path: HEIC文件路径

        Returns:
            PIL Image对象,失败返回None
        """
        try:
            if not self.validate_heic(file_path):
                print(f"文件验证失败: {file_path}")
                return None

            image = Image.open(file_path)
            # 转换为RGB模式以确保兼容性
            if image.mode != 'RGB':
                image = image.convert('RGB')

            return image
        except Exception as e:
            print(f"加载HEIC文件失败 {file_path}: {e}")
            return None

    def get_pil_image(self, file_path: str) -> Optional[Image.Image]:
        """
        获取PIL Image对象(load_heic的别名)

        Args:
            file_path: HEIC文件路径

        Returns:
            PIL Image对象,失败返回None
        """
        return self.load_heic(file_path)

    def get_thumbnail(self, file_path: str, size: Tuple[int, int] = (150, 150)) -> Optional[Image.Image]:
        """
        获取HEIC文件的缩略图

        Args:
            file_path: HEIC文件路径
            size: 缩略图尺寸 (width, height)

        Returns:
            缩略图Image对象,失败返回None
        """
        try:
            image = self.load_heic(file_path)
            if image is None:
                return None

            # 创建缩略图副本
            thumbnail = image.copy()
            thumbnail.thumbnail(size, Image.Resampling.LANCZOS)

            return thumbnail
        except Exception as e:
            print(f"生成缩略图失败 {file_path}: {e}")
            return None

    def get_exif_data(self, file_path: str) -> Dict[str, Any]:
        """
        获取HEIC文件的EXIF元数据

        Args:
            file_path: HEIC文件路径

        Returns:
            包含EXIF数据的字典
        """
        try:
            image = Image.open(file_path)
            exif_data = {}

            # 获取基本信息
            exif_data['format'] = image.format
            exif_data['mode'] = image.mode
            exif_data['size'] = image.size
            exif_data['width'] = image.width
            exif_data['height'] = image.height

            # 获取EXIF信息
            if hasattr(image, '_getexif') and image._getexif():
                exif = image._getexif()
                if exif:
                    exif_data['exif'] = exif

            # 获取info信息
            if hasattr(image, 'info'):
                exif_data['info'] = image.info

            return exif_data
        except Exception as e:
            print(f"获取EXIF数据失败 {file_path}: {e}")
            return {}

    def get_image_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取图像的详细信息

        Args:
            file_path: 图像文件路径

        Returns:
            包含图像信息的字典
        """
        try:
            info = {}

            # 文件信息
            if os.path.exists(file_path):
                info['file_name'] = os.path.basename(file_path)
                info['file_path'] = file_path
                info['file_size'] = os.path.getsize(file_path)
                info['file_size_mb'] = round(info['file_size'] / (1024 * 1024), 2)

            # 图像信息
            image = self.load_heic(file_path)
            if image:
                info['width'] = image.width
                info['height'] = image.height
                info['format'] = image.format
                info['mode'] = image.mode
                info['resolution'] = f"{image.width}x{image.height}"

            # EXIF信息
            exif_data = self.get_exif_data(file_path)
            if exif_data:
                info['exif'] = exif_data

            return info
        except Exception as e:
            print(f"获取图像信息失败 {file_path}: {e}")
            return {}


# 测试代码
if __name__ == "__main__":
    loader = HeicLoader()
    test_file = r"d:\7.project\heic-tools\heic-file\ES7210-ES8311音频.heic"

    if os.path.exists(test_file):
        print(f"测试文件: {test_file}")
        print(f"验证结果: {loader.validate_heic(test_file)}")

        image = loader.load_heic(test_file)
        if image:
            print(f"成功加载图像: {image.size}")

        info = loader.get_image_info(test_file)
        print(f"图像信息: {info}")
