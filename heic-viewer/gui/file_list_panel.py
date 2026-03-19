"""
文件列表面板组件
显示HEIC文件列表及缩略图
"""
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import List, Optional, Callable
import os
import threading


class FileListPanel(ctk.CTkScrollableFrame):
    """文件列表面板"""

    def __init__(self, master, heic_loader, on_file_select: Optional[Callable] = None, **kwargs):
        super().__init__(master, **kwargs)

        self.heic_loader = heic_loader
        self.on_file_select = on_file_select

        # 文件列表
        self.file_paths: List[str] = []
        self.file_items: List[dict] = []
        self.selected_index = -1

        # 缩略图缓存
        self.thumbnail_cache = {}

        # 配置网格
        self.grid_columnconfigure(0, weight=1)

    def add_file(self, file_path: str):
        """
        添加单个文件到列表

        Args:
            file_path: 文件路径
        """
        if file_path in self.file_paths:
            return

        self.file_paths.append(file_path)
        self._create_file_item(file_path, len(self.file_paths) - 1)

    def add_files(self, file_paths: List[str]):
        """
        添加多个文件到列表

        Args:
            file_paths: 文件路径列表
        """
        for file_path in file_paths:
            self.add_file(file_path)

    def remove_file(self, file_path: str):
        """
        从列表移除文件

        Args:
            file_path: 文件路径
        """
        if file_path in self.file_paths:
            index = self.file_paths.index(file_path)
            self.file_paths.remove(file_path)

            # 移除UI项
            if index < len(self.file_items):
                item = self.file_items.pop(index)
                item['frame'].destroy()

                # 更新后续项的索引
                for i in range(index, len(self.file_items)):
                    self.file_items[i]['index'] = i

    def clear_files(self):
        """清空文件列表"""
        self.file_paths.clear()

        # 销毁所有UI项
        for item in self.file_items:
            item['frame'].destroy()

        self.file_items.clear()
        self.selected_index = -1
        self.thumbnail_cache.clear()

    def select_file(self, index: int):
        """
        选择文件

        Args:
            index: 文件索引
        """
        if index < 0 or index >= len(self.file_paths):
            return

        # 取消之前的选择
        if 0 <= self.selected_index < len(self.file_items):
            self.file_items[self.selected_index]['frame'].configure(
                fg_color=("gray85", "gray25")
            )

        # 选中当前项
        self.selected_index = index
        self.file_items[index]['frame'].configure(
            fg_color=("gray75", "gray35")
        )

        # 触发回调
        if self.on_file_select:
            self.on_file_select(self.file_paths[index], index)

    def get_selected_file(self) -> Optional[str]:
        """获取当前选中的文件路径"""
        if 0 <= self.selected_index < len(self.file_paths):
            return self.file_paths[self.selected_index]
        return None

    def get_all_files(self) -> List[str]:
        """获取所有文件路径"""
        return self.file_paths.copy()

    def _create_file_item(self, file_path: str, index: int):
        """
        创建文件列表项

        Args:
            file_path: 文件路径
            index: 索引
        """
        # 创建容器框
        item_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray25"))
        item_frame.grid(row=index, column=0, padx=5, pady=2, sticky="ew")
        item_frame.grid_columnconfigure(1, weight=1)

        # 缩略图标签(占位)
        thumb_label = ctk.CTkLabel(
            item_frame,
            text="📄",
            width=60,
            height=60,
            font=("Arial", 30)
        )
        thumb_label.grid(row=0, column=0, padx=5, pady=5)

        # 文件名标签
        filename = os.path.basename(file_path)
        name_label = ctk.CTkLabel(
            item_frame,
            text=filename,
            anchor="w",
            wraplength=150
        )
        name_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 保存项信息
        item = {
            'frame': item_frame,
            'thumb_label': thumb_label,
            'name_label': name_label,
            'path': file_path,
            'index': index
        }
        self.file_items.append(item)

        # 绑定点击事件
        item_frame.bind("<Button-1>", lambda e, idx=index: self.select_file(idx))
        name_label.bind("<Button-1>", lambda e, idx=index: self.select_file(idx))

        # 在后台加载缩略图
        threading.Thread(
            target=self._load_thumbnail,
            args=(file_path, index),
            daemon=True
        ).start()

    def _load_thumbnail(self, file_path: str, index: int):
        """
        在后台加载缩略图

        Args:
            file_path: 文件路径
            index: 索引
        """
        try:
            # 检查缓存
            if file_path in self.thumbnail_cache:
                photo_image = self.thumbnail_cache[file_path]
            else:
                # 生成缩略图
                thumbnail = self.heic_loader.get_thumbnail(file_path, (60, 60))
                if thumbnail:
                    photo_image = ImageTk.PhotoImage(thumbnail)
                    self.thumbnail_cache[file_path] = photo_image
                else:
                    return

            # 更新UI(必须在主线程)
            if index < len(self.file_items):
                self.file_items[index]['thumb_label'].configure(
                    image=photo_image,
                    text=""
                )
                self.file_items[index]['thumb_label'].image = photo_image

        except Exception as e:
            print(f"加载缩略图失败 {file_path}: {e}")
