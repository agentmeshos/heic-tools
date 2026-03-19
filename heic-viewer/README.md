# HEIC图像查看器

一个基于Python的Windows桌面应用程序,用于查看和转换HEIC格式的图像文件。

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## 功能特性

- ✅ **HEIC文件查看**
  - 打开单个HEIC文件
  - 批量加载文件夹中的HEIC文件
  - 缩略图预览列表

- 🖼️ **图像浏览**
  - 高质量图像显示
  - 图像缩放(放大/缩小/适应窗口)
  - 鼠标拖拽移动
  - 鼠标滚轮缩放
  - 上一张/下一张切换

- 🔄 **格式转换**
  - 转换为JPG格式
  - 转换为PNG格式
  - 批量转换功能
  - 可调整JPG质量

- ⌨️ **快捷键支持**
  - `Ctrl+O`: 打开文件
  - `Ctrl+Shift+O`: 打开文件夹
  - `←/→`: 上一张/下一张
  - `+/-`: 放大/缩小
  - `Ctrl+0`: 重置缩放

## 系统要求

- **操作系统**: Windows 10/11
- **Python版本**: 3.8 或更高
- **内存**: 至少 2GB RAM
- **显示器**: 1280x720 或更高分辨率

## 安装步骤

### 1. 安装Python

从 [Python官网](https://www.python.org/downloads/) 下载并安装Python 3.8+

### 2. 克隆或下载项目

```bash
git clone <repository-url>
cd heic-viewer
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

依赖包列表:
- `customtkinter>=5.2.0` - 现代化UI组件
- `Pillow>=10.0.0` - 图像处理
- `pillow-heif>=0.13.0` - HEIC格式支持

## 使用方法

### 启动应用

```bash
python main.py
```

### 基本操作

1. **打开文件**
   - 点击工具栏的"打开文件"按钮
   - 或使用快捷键 `Ctrl+O`
   - 选择HEIC文件

2. **打开文件夹**
   - 点击"打开文件夹"按钮
   - 或使用快捷键 `Ctrl+Shift+O`
   - 选择包含HEIC文件的文件夹

3. **浏览图像**
   - 点击左侧文件列表切换图像
   - 使用"上一张"/"下一张"按钮
   - 使用键盘左右箭头键

4. **缩放和旋转图像**
   - 使用鼠标滚轮缩放
   - 点击"放大"/"缩小"按钮
   - 点击"适应窗口"自动调整大小
   - 点击"左转"/"右转"按钮旋转图像90度
   - 拖拽图像移动位置

5. **幻灯片播放**
   - 加载多个文件后
   - 点击"播放"按钮开始自动播放
   - 点击"暂停"按钮停止播放
   - 默认间隔3秒自动切换

6. **转换格式**
   - 打开HEIC文件后
   - 点击"转换为JPG"或"转换为PNG"
   - 选择保存位置

6. **批量转换**
   - 加载多个HEIC文件
   - 点击"批量转换"按钮
   - 选择输出目录和格式
   - 等待转换完成

## 项目结构

```
heic-viewer/
├── main.py                 # 应用程序入口
├── requirements.txt        # 依赖列表
├── README.md              # 本文档
├── gui/                   # GUI组件
│   ├── __init__.py
│   ├── main_window.py     # 主窗口
│   ├── image_canvas.py    # 图像显示组件
│   └── file_list_panel.py # 文件列表面板
├── core/                  # 核心功能
│   ├── __init__.py
│   ├── heic_loader.py     # HEIC加载器
│   ├── image_converter.py # 格式转换器
│   └── exif_reader.py     # EXIF读取器
└── utils/                 # 工具函数
    ├── __init__.py
    └── helpers.py         # 辅助函数
```

## 常见问题

### Q: 无法打开HEIC文件
A: 确保已正确安装 `pillow-heif` 包:
```bash
pip install pillow-heif --upgrade
```

### Q: 程序启动失败
A: 检查Python版本是否为3.8+:
```bash
python --version
```

### Q: 转换后的图像质量不佳
A: JPG转换默认质量为95,可以在代码中调整 `quality` 参数(1-100)。

### Q: 批量转换时程序无响应
A: 这是正常现象,程序正在后台处理文件。处理大量文件时请耐心等待。

### Q: 旋转后的图像无法保存
A: 转换时会自动保存旋转后的状态,确保已旋转后再进行转换操作。

### Q: 幻灯片播放速度太快或太慢
A: 默认间隔为3秒,可在代码中修改 `slideshow_interval` 值(单位毫秒)。

### 打包为可执行文件

使用PyInstaller打包:
```bash
pip install pyinstaller
pyinstaller "HEIC图像查看器.spec" --clean
```

生成的exe文件位于 `dist/` 目录,可以直接双击运行,无需Python环境。

**打包特点:**
- 单文件exe,方便分发
- 无需安装Python
- 包含所有依赖
- 文件大小约50-60MB

## 技术栈

- **GUI框架**: CustomTkinter (基于Tkinter)
- **图像处理**: Pillow (PIL)
- **HEIC支持**: pillow-heif
- **编程语言**: Python 3

## 开发说明

### 运行测试

测试HEIC加载器:
```bash
python core/heic_loader.py
```

测试图像转换:
```bash
python core/image_converter.py
```

测试工具函数:
```bash
python utils/helpers.py
```

### 打包为可执行文件

使用PyInstaller打包:
```bash
pip install pyinstaller
pyinstaller --name="HEIC图像查看器" --windowed --onefile main.py
```

生成的exe文件位于 `dist/` 目录。

## 许可证

本项目仅供学习和个人使用。

## 更新日志

### v1.1.0 (2026-02-14)
- ✨ 新增图像旋转功能(左转/右转90度)
- ✨ 新增幻灯片自动播放模式
- ✨ 转换时保存旋转后的图像状态
- ✅ 优化用户界面和控制按钮布局
- ✅ 成功打包为独立EXE可执行文件

### v1.0.0 (2026-02-14)
- ✨ 初始版本发布
- ✅ 基本的HEIC文件查看功能
- ✅ JPG/PNG格式转换
- ✅ 批量处理支持
- ✅ 现代化UI界面
- ✅ 快捷键支持

## 联系方式

如有问题或建议,请提交Issue或Pull Request。

---

**享受使用HEIC图像查看器!** 🎉
