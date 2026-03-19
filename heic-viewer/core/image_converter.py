"""
图像格式转换器
负责将HEIC文件转换为JPG、PNG等常见格式
"""
import os
from pathlib import Path
from typing import Optional, List, Tuple, Callable
from PIL import Image
from core.heic_loader import HeicLoader


class ImageConverter:
    """图像格式转换器类"""

    def __init__(self):
        """初始化转换器"""
        self.heic_loader = HeicLoader()

    def convert_to_jpg(self, input_path: str, output_path: Optional[str] = None,
                      quality: int = 95) -> Tuple[bool, str]:
        """
        将HEIC文件转换为JPG格式

        Args:
            input_path: 输入HEIC文件路径
            output_path: 输出JPG文件路径,None则自动生成
            quality: JPG质量(1-100),默认95

        Returns:
            (成功标志, 输出文件路径或错误信息)
        """
        try:
            # 加载HEIC图像
            image = self.heic_loader.load_heic(input_path)
            if image is None:
                return False, "加载HEIC文件失败"

            # 生成输出路径
            if output_path is None:
                output_path = self._get_output_path(input_path, "jpg")

            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 转换为RGB模式(JPG不支持透明度)
            if image.mode in ('RGBA', 'LA', 'P'):
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                image = rgb_image
            elif image.mode != 'RGB':
                image = image.convert('RGB')

            # 保存为JPG
            image.save(output_path, 'JPEG', quality=quality, optimize=True)

            return True, output_path
        except Exception as e:
            return False, f"转换失败: {str(e)}"

    def convert_to_png(self, input_path: str, output_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        将HEIC文件转换为PNG格式

        Args:
            input_path: 输入HEIC文件路径
            output_path: 输出PNG文件路径,None则自动生成

        Returns:
            (成功标志, 输出文件路径或错误信息)
        """
        try:
            # 加载HEIC图像
            image = self.heic_loader.load_heic(input_path)
            if image is None:
                return False, "加载HEIC文件失败"

            # 生成输出路径
            if output_path is None:
                output_path = self._get_output_path(input_path, "png")

            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 保存为PNG(保留所有信息)
            image.save(output_path, 'PNG', optimize=True)

            return True, output_path
        except Exception as e:
            return False, f"转换失败: {str(e)}"

    def batch_convert(self, file_list: List[str], output_dir: str,
                     format: str = 'jpg', quality: int = 95,
                     progress_callback: Optional[Callable[[int, int, str], None]] = None) -> List[Tuple[str, bool, str]]:
        """
        批量转换HEIC文件

        Args:
            file_list: HEIC文件路径列表
            output_dir: 输出目录
            format: 输出格式('jpg'或'png')
            quality: JPG质量(仅当format='jpg'时有效)
            progress_callback: 进度回调函数(当前索引, 总数, 当前文件名)

        Returns:
            结果列表[(文件路径, 成功标志, 输出路径或错误信息)]
        """
        results = []
        total = len(file_list)

        for index, input_path in enumerate(file_list):
            try:
                # 调用进度回调
                if progress_callback:
                    progress_callback(index + 1, total, os.path.basename(input_path))

                # 生成输出路径
                filename = os.path.basename(input_path)
                name_without_ext = os.path.splitext(filename)[0]
                output_path = os.path.join(output_dir, f"{name_without_ext}.{format}")

                # 根据格式选择转换方法
                if format.lower() == 'jpg' or format.lower() == 'jpeg':
                    success, message = self.convert_to_jpg(input_path, output_path, quality)
                elif format.lower() == 'png':
                    success, message = self.convert_to_png(input_path, output_path)
                else:
                    success = False
                    message = f"不支持的格式: {format}"

                results.append((input_path, success, message))

            except Exception as e:
                results.append((input_path, False, f"处理失败: {str(e)}"))

        return results

    def _get_output_path(self, input_path: str, format: str) -> str:
        """
        生成输出文件路径

        Args:
            input_path: 输入文件路径
            format: 输出格式(jpg/png)

        Returns:
            输出文件路径
        """
        path = Path(input_path)
        return str(path.parent / f"{path.stem}.{format}")

    def get_output_filename(self, input_filename: str, format: str) -> str:
        """
        生成输出文件名

        Args:
            input_filename: 输入文件名
            format: 输出格式

        Returns:
            输出文件名
        """
        name_without_ext = os.path.splitext(input_filename)[0]
        return f"{name_without_ext}.{format}"


# 测试代码
if __name__ == "__main__":
    converter = ImageConverter()
    test_file = r"d:\7.project\heic-tools\heic-file\ES7210-ES8311音频.heic"

    if os.path.exists(test_file):
        print(f"测试转换: {test_file}")

        # 测试转为JPG
        output_dir = r"d:\7.project\heic-tools\heic-viewer\test_output"
        os.makedirs(output_dir, exist_ok=True)

        jpg_path = os.path.join(output_dir, "test_output.jpg")
        success, message = converter.convert_to_jpg(test_file, jpg_path, quality=90)
        print(f"JPG转换: {'成功' if success else '失败'} - {message}")

        # 测试转为PNG
        png_path = os.path.join(output_dir, "test_output.png")
        success, message = converter.convert_to_png(test_file, png_path)
        print(f"PNG转换: {'成功' if success else '失败'} - {message}")
