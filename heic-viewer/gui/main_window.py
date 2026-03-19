"""
主窗口
HEIC图像查看器的主界面
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.image_canvas import ImageCanvas
from gui.file_list_panel import FileListPanel
from core.heic_loader import HeicLoader
from core.image_converter import ImageConverter
from core.exif_reader import ExifReader
from utils.helpers import get_heic_files, format_file_size


class MainWindow(ctk.CTk):
    """主窗口类"""

    def __init__(self):
        super().__init__()

        # 窗口设置
        self.title("HEIC图像查看器")
        self.geometry("1200x800")

        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 核心组件
        self.heic_loader = HeicLoader()
        self.converter = ImageConverter()
        self.exif_reader = ExifReader()

        # 当前状态
        self.current_file = None
        self.current_index = -1
        
        # 幻灯片播放
        self.slideshow_playing = False
        self.slideshow_interval = 3000  # 3秒
        self.slideshow_timer_id = None

        # 创建UI
        self.setup_ui()
        self.bind_shortcuts()

    def setup_ui(self):
        """初始化UI布局"""
        # 配置网格
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 创建工具栏
        self.create_toolbar()

        # 创建文件列表面板
        self.create_file_panel()

        # 创建图像显示区
        self.create_image_panel()

        # 创建状态栏
        self.create_status_bar()

    def create_toolbar(self):
        """创建工具栏"""
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # 打开文件按钮
        btn_open_file = ctk.CTkButton(
            toolbar,
            text="打开文件",
            command=self.load_file,
            width=100
        )
        btn_open_file.pack(side="left", padx=5)

        # 打开文件夹按钮
        btn_open_folder = ctk.CTkButton(
            toolbar,
            text="打开文件夹",
            command=self.load_folder,
            width=100
        )
        btn_open_folder.pack(side="left", padx=5)

        # 分隔符
        separator1 = ctk.CTkLabel(toolbar, text="|", width=20)
        separator1.pack(side="left", padx=5)

        # 转换为JPG按钮
        btn_to_jpg = ctk.CTkButton(
            toolbar,
            text="转换为JPG",
            command=lambda: self.convert_current('jpg'),
            width=100
        )
        btn_to_jpg.pack(side="left", padx=5)

        # 转换为PNG按钮
        btn_to_png = ctk.CTkButton(
            toolbar,
            text="转换为PNG",
            command=lambda: self.convert_current('png'),
            width=100
        )
        btn_to_png.pack(side="left", padx=5)

        # 批量转换按钮
        btn_batch = ctk.CTkButton(
            toolbar,
            text="批量转换",
            command=self.batch_convert,
            width=100
        )
        btn_batch.pack(side="left", padx=5)
        
        # 分隔符
        separator_ss = ctk.CTkLabel(toolbar, text="|", width=20)
        separator_ss.pack(side="left", padx=5)
        
        # 幻灯片播放按钮
        self.btn_slideshow = ctk.CTkButton(
            toolbar,
            text="▶ 播放",
            command=self.toggle_slideshow,
            width=100
        )
        self.btn_slideshow.pack(side="left", padx=5)

    def create_file_panel(self):
        """创建文件列表面板"""
        self.file_panel = FileListPanel(
            self,
            heic_loader=self.heic_loader,
            on_file_select=self.on_file_selected,
            width=250
        )
        self.file_panel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def create_image_panel(self):
        """创建图像显示面板"""
        # 图像容器
        image_container = ctk.CTkFrame(self)
        image_container.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        image_container.grid_rowconfigure(0, weight=1)
        image_container.grid_columnconfigure(0, weight=1)

        # 图像画布
        self.image_canvas = ImageCanvas(image_container)
        self.image_canvas.grid(row=0, column=0, sticky="nsew")

        # 控制栏
        control_bar = ctk.CTkFrame(image_container, height=50)
        control_bar.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # 上一张按钮
        btn_prev = ctk.CTkButton(
            control_bar,
            text="◀ 上一张",
            command=self.prev_image,
            width=100
        )
        btn_prev.pack(side="left", padx=5)

        # 下一张按钮
        btn_next = ctk.CTkButton(
            control_bar,
            text="下一张 ▶",
            command=self.next_image,
            width=100
        )
        btn_next.pack(side="left", padx=5)
        
        # 分隔符
        separator2 = ctk.CTkLabel(control_bar, text="|", width=20)
        separator2.pack(side="left", padx=5)

        # 缩放按钮
        btn_zoom_in = ctk.CTkButton(
            control_bar,
            text="放大 +",
            command=self.image_canvas.zoom_in,
            width=80
        )
        btn_zoom_in.pack(side="left", padx=5)

        btn_zoom_out = ctk.CTkButton(
            control_bar,
            text="缩小 -",
            command=self.image_canvas.zoom_out,
            width=80
        )
        btn_zoom_out.pack(side="left", padx=5)

        btn_reset = ctk.CTkButton(
            control_bar,
            text="重置",
            command=self.image_canvas.reset_zoom,
            width=80
        )
        btn_reset.pack(side="left", padx=5)

        btn_fit = ctk.CTkButton(
            control_bar,
            text="适应窗口",
            command=self.image_canvas.fit_to_window,
            width=80
        )
        btn_fit.pack(side="left", padx=5)
        
        # 分隔符
        separator3 = ctk.CTkLabel(control_bar, text="|", width=20)
        separator3.pack(side="left", padx=5)
        
        # 旋转按钮
        btn_rotate_left = ctk.CTkButton(
            control_bar,
            text="↶ 左转",
            command=self.image_canvas.rotate_left,
            width=80
        )
        btn_rotate_left.pack(side="left", padx=5)
        
        btn_rotate_right = ctk.CTkButton(
            control_bar,
            text="右转 ↷",
            command=self.image_canvas.rotate_right,
            width=80
        )
        btn_rotate_right.pack(side="left", padx=5)

    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = ctk.CTkFrame(self, height=30)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="就绪",
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, fill="x", expand=True)

    def bind_shortcuts(self):
        """绑定快捷键"""
        self.bind("<Left>", lambda e: self.prev_image())
        self.bind("<Right>", lambda e: self.next_image())
        self.bind("<Control-o>", lambda e: self.load_file())
        self.bind("<Control-Shift-O>", lambda e: self.load_folder())
        self.bind("<plus>", lambda e: self.image_canvas.zoom_in())
        self.bind("<minus>", lambda e: self.image_canvas.zoom_out())
        self.bind("<Control-0>", lambda e: self.image_canvas.reset_zoom())

    def load_file(self):
        """打开单个文件"""
        file_path = filedialog.askopenfilename(
            title="选择HEIC文件",
            filetypes=[("HEIC文件", "*.heic *.heif"), ("所有文件", "*.*")]
        )

        if file_path:
            self.file_panel.clear_files()
            self.file_panel.add_file(file_path)
            self.file_panel.select_file(0)

    def load_folder(self):
        """打开文件夹"""
        folder_path = filedialog.askdirectory(title="选择文件夹")

        if folder_path:
            heic_files = get_heic_files(folder_path)
            if heic_files:
                self.file_panel.clear_files()
                self.file_panel.add_files(heic_files)
                self.update_status(f"加载了 {len(heic_files)} 个文件")
            else:
                messagebox.showinfo("提示", "该文件夹中没有找到HEIC文件")

    def on_file_selected(self, file_path: str, index: int):
        """
        文件选中回调

        Args:
            file_path: 文件路径
            index: 索引
        """
        self.current_file = file_path
        self.current_index = index
        self.show_image(file_path)

    def show_image(self, file_path: str):
        """
        显示图像

        Args:
            file_path: 文件路径
        """
        try:
            # 加载图像
            image = self.heic_loader.load_heic(file_path)
            if image:
                self.image_canvas.load_image(image)
                self.update_status_info(file_path)
            else:
                messagebox.showerror("错误", f"无法加载文件: {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"加载失败: {str(e)}")

    def next_image(self):
        """下一张"""
        files = self.file_panel.get_all_files()
        if not files:
            return

        next_index = (self.current_index + 1) % len(files)
        self.file_panel.select_file(next_index)

    def prev_image(self):
        """上一张"""
        files = self.file_panel.get_all_files()
        if not files:
            return

        prev_index = (self.current_index - 1) % len(files)
        self.file_panel.select_file(prev_index)

    def convert_current(self, format: str):
        """
        转换当前文件

        Args:
            format: 目标格式
        """
        if not self.current_file:
            messagebox.showwarning("提示", "请先打开一个HEIC文件")
            return

        output_path = filedialog.asksaveasfilename(
            title=f"保存为{format.upper()}",
            defaultextension=f".{format}",
            filetypes=[(f"{format.upper()}文件", f"*.{format}")]
        )

        if output_path:
            try:
                # 获取旋转后的图像
                rotated_image = self.image_canvas.get_rotated_image()
                if rotated_image is None:
                    messagebox.showerror("错误", "无法获取图像")
                    return
                
                # 保存旋转后的图像
                if format == 'jpg':
                    if rotated_image.mode in ('RGBA', 'LA', 'P'):
                        rgb_image = Image.new('RGB', rotated_image.size, (255, 255, 255))
                        if rotated_image.mode == 'P':
                            rotated_image = rotated_image.convert('RGBA')
                        rgb_image.paste(rotated_image, mask=rotated_image.split()[-1] if rotated_image.mode in ('RGBA', 'LA') else None)
                        rotated_image = rgb_image
                    elif rotated_image.mode != 'RGB':
                        rotated_image = rotated_image.convert('RGB')
                    rotated_image.save(output_path, 'JPEG', quality=95, optimize=True)
                    success, message = True, output_path
                else:
                    rotated_image.save(output_path, 'PNG', optimize=True)
                    success, message = True, output_path

                if success:
                    messagebox.showinfo("成功", f"已保存到: {output_path}")
                else:
                    messagebox.showerror("失败", message)
            except Exception as e:
                messagebox.showerror("错误", f"转换失败: {str(e)}")

    def batch_convert(self):
        """批量转换"""
        files = self.file_panel.get_all_files()
        if not files:
            messagebox.showwarning("提示", "请先加载HEIC文件")
            return

        # 选择输出目录
        output_dir = filedialog.askdirectory(title="选择输出目录")
        if not output_dir:
            return

        # 选择格式
        format_window = ctk.CTkToplevel(self)
        format_window.title("选择格式")
        format_window.geometry("300x150")
        format_window.transient(self)
        format_window.grab_set()

        selected_format = ctk.StringVar(value="jpg")

        ctk.CTkLabel(format_window, text="选择输出格式:", font=("Arial", 14)).pack(pady=10)
        ctk.CTkRadioButton(format_window, text="JPG", variable=selected_format, value="jpg").pack(pady=5)
        ctk.CTkRadioButton(format_window, text="PNG", variable=selected_format, value="png").pack(pady=5)

        def start_convert():
            format = selected_format.get()
            format_window.destroy()

            # 执行转换
            results = self.converter.batch_convert(files, output_dir, format)

            # 统计结果
            success_count = sum(1 for _, success, _ in results if success)
            fail_count = len(results) - success_count

            messagebox.showinfo(
                "完成",
                f"批量转换完成!\n成功: {success_count}\n失败: {fail_count}"
            )

        ctk.CTkButton(format_window, text="开始转换", command=start_convert).pack(pady=10)

    def update_status(self, message: str):
        """更新状态栏消息"""
        self.status_label.configure(text=message)

    def update_status_info(self, file_path: str):
        """更新状态栏图像信息"""
        try:
            filename = os.path.basename(file_path)
            file_size = format_file_size(os.path.getsize(file_path))

            image = self.heic_loader.load_heic(file_path)
            if image:
                resolution = f"{image.width}x{image.height}"
                zoom = self.image_canvas.get_zoom_percent()
                self.update_status(
                    f"{filename} | {file_size} | {resolution} | 缩放: {zoom}%"
                )
        except:
            pass
    
    def toggle_slideshow(self):
        """切换幻灯片播放状态"""
        if self.slideshow_playing:
            self.stop_slideshow()
        else:
            self.start_slideshow()
    
    def start_slideshow(self):
        """开始幻灯片播放"""
        files = self.file_panel.get_all_files()
        if not files or len(files) < 2:
            messagebox.showwarning("提示", "请至少加载2个文件")
            return
        
        self.slideshow_playing = True
        self.btn_slideshow.configure(text="⏸ 暂停")
        self._slideshow_next()
    
    def stop_slideshow(self):
        """停止幻灯片播放"""
        self.slideshow_playing = False
        self.btn_slideshow.configure(text="▶ 播放")
        if self.slideshow_timer_id:
            self.after_cancel(self.slideshow_timer_id)
            self.slideshow_timer_id = None
    
    def _slideshow_next(self):
        """播放下一张"""
        if not self.slideshow_playing:
            return
        
        self.next_image()
        self.slideshow_timer_id = self.after(
            self.slideshow_interval,
            self._slideshow_next
        )


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
