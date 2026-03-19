"""
EXIF信息读取器
负责读取和解析图像文件的EXIF元数据
"""
from typing import Dict, Any, Optional
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os


class ExifReader:
    """EXIF信息读取器类"""

    @staticmethod
    def get_exif_data(image_path: str) -> Dict[str, Any]:
        """
        获取图像的EXIF数据

        Args:
            image_path: 图像文件路径

        Returns:
            包含EXIF信息的字典
        """
        try:
            exif_data = {}

            with Image.open(image_path) as image:
                # 基本信息
                exif_data['file_name'] = os.path.basename(image_path)
                exif_data['format'] = image.format
                exif_data['mode'] = image.mode
                exif_data['size'] = image.size
                exif_data['width'] = image.width
                exif_data['height'] = image.height

                # 获取EXIF标签
                exif = image.getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        exif_data[tag_name] = value

                    # 获取GPS信息
                    gps_info = exif.get_ifd(0x8825)
                    if gps_info:
                        gps_data = {}
                        for tag_id, value in gps_info.items():
                            tag_name = GPSTAGS.get(tag_id, tag_id)
                            gps_data[tag_name] = value
                        exif_data['GPSInfo'] = gps_data

            return exif_data
        except Exception as e:
            print(f"读取EXIF失败 {image_path}: {e}")
            return {}

    @staticmethod
    def get_readable_exif(image_path: str) -> Dict[str, str]:
        """
        获取可读性强的EXIF信息

        Args:
            image_path: 图像文件路径

        Returns:
            格式化后的EXIF信息字典
        """
        exif_data = ExifReader.get_exif_data(image_path)
        readable = {}

        # 基本信息
        if 'file_name' in exif_data:
            readable['文件名'] = exif_data['file_name']
        if 'format' in exif_data:
            readable['格式'] = exif_data['format']
        if 'width' in exif_data and 'height' in exif_data:
            readable['分辨率'] = f"{exif_data['width']}x{exif_data['height']}"

        # 相机信息
        if 'Make' in exif_data:
            readable['制造商'] = exif_data['Make']
        if 'Model' in exif_data:
            readable['型号'] = exif_data['Model']
        if 'LensModel' in exif_data:
            readable['镜头'] = exif_data['LensModel']

        # 拍摄参数
        if 'DateTime' in exif_data:
            readable['拍摄时间'] = exif_data['DateTime']
        if 'DateTimeOriginal' in exif_data:
            readable['原始时间'] = exif_data['DateTimeOriginal']
        if 'ExposureTime' in exif_data:
            readable['曝光时间'] = ExifReader._format_exposure_time(exif_data['ExposureTime'])
        if 'FNumber' in exif_data:
            readable['光圈'] = f"f/{exif_data['FNumber']}"
        if 'ISOSpeedRatings' in exif_data:
            readable['ISO'] = str(exif_data['ISOSpeedRatings'])
        if 'FocalLength' in exif_data:
            readable['焦距'] = f"{exif_data['FocalLength']}mm"
        if 'Flash' in exif_data:
            readable['闪光灯'] = '开启' if exif_data['Flash'] else '关闭'

        # 软件信息
        if 'Software' in exif_data:
            readable['软件'] = exif_data['Software']

        return readable

    @staticmethod
    def _format_exposure_time(value) -> str:
        """格式化曝光时间"""
        try:
            if isinstance(value, tuple):
                numerator, denominator = value
                if numerator < denominator:
                    return f"1/{int(denominator/numerator)}"
                return f"{numerator/denominator}"
            return str(value)
        except:
            return str(value)


# 测试代码
if __name__ == "__main__":
    test_file = r"d:\7.project\heic-tools\heic-file\ES7210-ES8311音频.heic"

    if os.path.exists(test_file):
        print("=== EXIF详细信息 ===")
        exif_data = ExifReader.get_exif_data(test_file)
        for key, value in list(exif_data.items())[:10]:
            print(f"{key}: {value}")

        print("\n=== 可读EXIF信息 ===")
        readable = ExifReader.get_readable_exif(test_file)
        for key, value in readable.items():
            print(f"{key}: {value}")
