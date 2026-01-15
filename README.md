# 音频处理工具箱 🎵

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于 Python 和 PyQt5 的音频处理工具箱，提供直观的图形界面和音频处理功能。
## 图形界面
<img width="865" height="513" alt="image" src="https://github.com/user-attachments/assets/cdaaac4f-7e81-45e4-883f-b0be996f68bf" />

## 🎵 效果演示
- 原始音频
  
https://github.com/user-attachments/assets/5ec4ab30-fd9a-49c0-9343-76f61eeb88eb

- 加速后音频

https://github.com/user-attachments/assets/63fb76d4-26d1-48b1-9584-70618af50e40


- 变音后音频



https://github.com/user-attachments/assets/916caa0a-4011-49fa-a754-4f1743535998


  
- 原始音频带噪声



https://github.com/user-attachments/assets/af327683-b365-43e9-9527-acf765811182


  
- 音频带噪声去噪后



https://github.com/user-attachments/assets/817a303d-c410-430a-b8e0-4e470f7f6d38



## ✨ 功能特性

### 🎤 音频变换工具
- **变声功能**: 音高调整（±12半音），实现升调/降调效果
- **语速调整**: 0.5x - 2.0x 倍速，音高保持不变
- **回声效果**: 自定义延迟时间和衰减系数

### ✂️ 音频编辑工具
- **精确切分**: 按时间段截取音频片段
- **智能静音**: 自动去除首尾静音和长静音段
- **采样率调整**: 支持 8kHz - 48kHz 多种采样率
- **声道转换**: 单声道⇄立体声自由转换

### 🔇 语音降噪工具
- **频谱减法降噪**: 有效减少背景噪声
- **参数可调**: 降噪强度和噪声门限可自由设置
- **实时预览**: 波形可视化显示处理效果

### 📊 可视化功能
- **实时波形显示**: 基于 PyQtGraph 的高性能波形绘制
- **深色主题**: 专业音频软件风格界面
- **参数直观**: 滑块、旋钮等直观的参数控制

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

或使用国内镜像加速：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 运行程序

**所有平台**：
```bash
python main.py
```

## 💡 使用示例

### GUI界面使用

1. **加载音频**: 点击"加载音频"选择文件
2. **选择工具**: 在左侧工具列表中选择功能
3. **调整参数**: 在右侧面板设置参数
4. **执行处理**: 点击"应用XXX"按钮
5. **保存结果**: 点击"保存音频"导出

## 🎯 支持格式

- **输入**: WAV, MP3, FLAC, OGG, M4A
- **输出**: WAV, FLAC, OGG

## 🛠️ 技术栈

- **GUI框架**: PyQt5
- **数值计算**: NumPy, SciPy
- **音频处理**: Librosa, SoundFile
- **可视化**: PyQtGraph, Matplotlib

## 📁 项目结构

```
audio_tools/
├── main.py                    # 主程序入口
├── main_window.py             # 主窗口类
├── run.bat                    # Windows启动脚本
├── requirements.txt           # 依赖包列表
│
├── modules/                   # 功能模块
│   ├── audio_io.py           # 音频I/O
│   ├── audio_changer.py      # 音频变换
│   ├── audio_editor.py       # 音频编辑
│   └── audio_noise_remover.py # 降噪处理
│
|── ui/                        # 界面相关
    ├── waveform_widget.py    # 波形显示
    └── tool_panels.py        # 工具面板

```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件

## 🌟 特别感谢

- [Librosa](https://librosa.org/) - 强大的音频分析库
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 优秀的GUI框架
- [PyQtGraph](http://www.pyqtgraph.org/) - 高性能绘图库

## 📮 联系方式

- 项目主页: [GitHub](https://github.com/study-233/Audio-Processing-Toolbox)
- 问题反馈: [Issues](https://github.com/study-233/Audio-Processing-Toolbox/issues)

---

**如果这个项目对您有帮助，请给一个 ⭐ Star！**
