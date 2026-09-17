# 📷 HEIC 文件工具集

> Windows 平台 HEIC 图像格式处理工具集

本仓库包含用于处理 HEIC（High Efficiency Image Container）格式图像的 Windows 桌面工具，主要针对 iPhone/iPad 等 Apple 设备拍摄的 HEIC 格式照片。

---

## 📋 项目概述

HEIC 是 Apple 设备默认使用的高效图像格式，相比 JPEG 具有更好的压缩率和画质。本项目提供 Windows 平台下的 HEIC 文件查看和处理能力。

### 🎯 目标用户

需要在 Windows 系统上查看、浏览或处理 iPhone/iPad 等设备拍摄的 HEIC 格式照片的用户。

---

## 📁 项目结构

```
heic-tools/
├── heic-viewer/          # HEIC 图像查看器（Python WPF 应用）
│   └── (查看器源代码和资源)
├── heic-file/            # HEIC 测试文件集
│   └── (5个测试用 HEIC 文件)
└── 规划书.md             # 项目规划文档
```

---

## 🛠️ 子项目说明

### 1. heic-viewer - HEIC 图像查看器

**类型**：Windows GUI 桌面应用程序  
**技术栈**：Python + WPF  
**功能**：
- ✅ 文件浏览：支持选择单个 HEIC 文件或文件夹批量加载
- ✅ 图像查看：显示 HEIC 图像完整内容，自适应窗口大小
- ✅ 图像操作：支持缩放（放大/缩小/还原）、拖拽移动
- ✅ 文件导航：上一张/下一张切换，支持快捷键（左右箭头）
- ✅ 图像转换：转换为常见格式（JPG/PNG），支持批量转换
- ✅ 友好界面：提供直观的用户界面和基本操作功能

### 2. heic-file - 测试文件集

**用途**：提供 HEIC 格式测试文件，用于验证查看器功能

**包含文件**：
- ES7210-ES8311音频.heic
- GigoDevice 25Q32CS1G 32Mflash.heic
- RT9048-GSPABBK5电源.heic
- 互联接口-radar.heic
- 互联接口MCU.heic

---

## 🚀 使用场景

1. **快速查看**：在 Windows 上直接打开 HEIC 照片，无需转换
2. **批量浏览**：文件夹模式快速浏览多张 HEIC 照片
3. **格式转换**：将 HEIC 照片批量转换为 JPG/PNG 格式
4. **跨平台共享**：转换后的照片可在更多设备和应用中使用

---

## 📖 文档

详细的功能需求、技术选型和开发计划请查看 `规划书.md`

---

## 💡 技术说明

HEIC 格式由 HEIF（High Efficiency Image Format）标准定义，使用 HEVC（H.265）编码实现高效压缩。本项目利用 Python 生态系统中的 HEIC 解码库，为 Windows 用户提供原生的查看体验。
