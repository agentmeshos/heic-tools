"""
图像画布组件
负责显示图像并支持缩放、拖拽等交互
"""
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Optional
import tkinter as tk


class ImageCanvas(ctk.CTkFrame):
    """图像显示画布组件"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # 画布变量
        self.pil_image: Optional[Image.Image] = None
        self.display_image: Optional[ImageTk.PhotoImage] = None
        self.zoom_level = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        self.zoom_step = 0.1
        self.rotation_angle = 0  # 旋转角度(0, 90, 180, 270)

        # 拖拽变量
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging = False

        # 创建Canvas
        self.canvas = tk.Canvas(
            self,
            bg="#2b2b2b",
            highlightthickness=0,
            cursor="cross"
        )
        self.canvas.pack(fill="both", expand=True)

        # 图像ID
        self.image_id = None

        # 绑定事件
        self._bind_events()

    def _bind_events(self):
        """绑定鼠标事件"""
        # 鼠标滚轮缩放
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)

        # 拖拽
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_drag_end)

        # 窗口大小变化
        self.canvas.bind("<Configure>", self._on_resize)

    def load_image(self, pil_image: Image.Image):
        """
        加载并显示图像

        Args:
            pil_image: PIL Image对象
        """
        if pil_image is None:
            return

        self.pil_image = pil_image
        self.zoom_level = 1.0
        self.fit_to_window()

    def fit_to_window(self):
        """适应窗口大小显示图像"""
        if self.pil_image is None:
            return

        # 获取画布大小
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        # 计算缩放比例
        img_width, img_height = self.pil_image.size
        width_ratio = canvas_width / img_width
        height_ratio = canvas_height / img_height
        self.zoom_level = min(width_ratio, height_ratio) * 0.95

        self._update_display()

    def zoom_in(self):
        """放大图像"""
        if self.pil_image is None:
            return

        self.zoom_level = min(self.zoom_level + self.zoom_step, self.max_zoom)
        self._update_display()

    def zoom_out(self):
        """缩小图像"""
        if self.pil_image is None:
            return

        self.zoom_level = max(self.zoom_level - self.zoom_step, self.min_zoom)
        self._update_display()

    def reset_zoom(self):
        """重置缩放到100%"""
        if self.pil_image is None:
            return

        self.zoom_level = 1.0
        self._update_display()

    def get_zoom_percent(self) -> int:
        """获取当前缩放百分比"""
        return int(self.zoom_level * 100)
    
    def rotate_left(self):
        """逆时针旋转90度"""
        if self.pil_image is None:
            return
        
        self.rotation_angle = (self.rotation_angle - 90) % 360
        self._update_display()
    
    def rotate_right(self):
        """顺时针旋转90度"""
        if self.pil_image is None:
            return
        
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self._update_display()
    
    def get_rotated_image(self) -> Optional[Image.Image]:
        """获取旋转后的图像"""
        if self.pil_image is None:
            return None
        
        if self.rotation_angle == 0:
            return self.pil_image
        else:
            return self.pil_image.rotate(-self.rotation_angle, expand=True)

    def _update_display(self):
        """更新图像显示"""
        if self.pil_image is None:
            return

        try:
            # 应用旋转
            display_img = self.pil_image
            if self.rotation_angle != 0:
                display_img = self.pil_image.rotate(-self.rotation_angle, expand=True)
            
            # 计算缩放后的尺寸
            img_width, img_height = display_img.size
            new_width = int(img_width * self.zoom_level)
            new_height = int(img_height * self.zoom_level)

            # 缩放图像
            resized_image = display_img.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

            # 转换为PhotoImage
            self.display_image = ImageTk.PhotoImage(resized_image)

            # 清除旧图像
            self.canvas.delete("all")

            # 在画布中心显示图像
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            x = canvas_width // 2
            y = canvas_height // 2

            self.image_id = self.canvas.create_image(
                x, y,
                image=self.display_image,
                anchor="center"
            )

        except Exception as e:
            print(f"更新显示失败: {e}")

    def _on_mouse_wheel(self, event):
        """鼠标滚轮事件处理"""
        if self.pil_image is None:
            return

        # Windows系统
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def _on_drag_start(self, event):
        """开始拖拽"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.is_dragging = True
        self.canvas.config(cursor="fleur")

    def _on_drag_motion(self, event):
        """拖拽移动"""
        if not self.is_dragging or self.image_id is None:
            return

        # 计算偏移量
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        # 移动图像
        self.canvas.move(self.image_id, dx, dy)

        # 更新起始位置
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _on_drag_end(self, event):
        """结束拖拽"""
        self.is_dragging = False
        self.canvas.config(cursor="cross")

    def _on_resize(self, event):
        """窗口大小变化"""
        # 如果图像已加载,重新居中显示
        if self.pil_image is not None and self.image_id is not None:
            self._update_display()

    def clear(self):
        """清空画布"""
        self.canvas.delete("all")
        self.pil_image = None
        self.display_image = None
        self.zoom_level = 1.0
        self.rotation_angle = 0
