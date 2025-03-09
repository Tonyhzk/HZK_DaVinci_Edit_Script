# HZK 达芬奇剪辑脚本 / HZK DaVinci Resolve Editing Script

## 简介 / Introduction

HZK 达芬奇剪辑脚本是一个基于 Python 和 Tkinter 开发的 GUI 工具，专为 **DaVinci Resolve** 设计，旨在帮助视频剪辑师自动化处理时间线中的音频和视频片段，提高剪辑效率。

HZK DaVinci Resolve Editing Script is a GUI tool developed with Python and Tkinter, specifically designed for **DaVinci Resolve**. It helps video editors automate the processing of audio and video clips in the timeline, improving editing efficiency.

---

## 功能 / Features

✅ **删除未启用的音频/视频片段**<br />✅ **删除已启用的音频/视频片段**<br />✅ **删除离线的音频/视频片段**<br />✅ **切换音频/视频片段的启用状态**<br />✅ **实时日志输出**

✅ **Delete disabled audio/video clips**<br />✅ **Delete enabled audio/video clips**<br />✅ **Delete offline audio/video clips**<br />✅ **Toggle enable/disable state of audio/video clips**<br />✅ **Real-time log output**

---

## 安装 / Installation

### 1. 确保你的系统已安装 Python 3

请访问 [Python 官网](https://www.python.org/) 下载并安装 Python 3。

### 2. 安装 Tkinter（通常已内置）

Tkinter 是 Python 的标准 GUI 库，一般情况下已随 Python 安装。如果 Tkinter 未安装，可使用以下命令安装：

```bash
# Windows
pip install tk

# macOS / Linux
sudo apt-get install python3-tk  # Ubuntu/Debian
brew install python-tk           # macOS (使用 Homebrew)
```

### 3. 配置 DaVinci Resolve 脚本支持

确保你的 DaVinci Resolve **Scripting API** 已正确配置：

1. **打开 DaVinci Resolve**
2. **前往** **​`首选项 -> 系统 -> 常规`​**
3. **启用** **​`外部脚本访问`​** **并选择** **​`本机 + 远程`​**
4. **重启 DaVinci Resolve 以应用更改**

---

## 使用 / Usage

### 1. 运行脚本

```bash
python script.py
```

### 2. 选择操作

启动 GUI 后，选择需要执行的操作：

* **删除未启用的音频/视频**
* **删除已启用的音频/视频**
* **删除离线的音频/视频**
* **切换音频/视频的启用状态**

### 3. 查看日志

操作结果将在 GUI 下方的日志窗口中显示。

---

## 截图 / Screenshots

![Snipaste_2025-03-09_17-23-38](Pic/Snipaste_2025-03-09_17-23-38-20250309172417.png)

---

## 贡献 / Contributing

如果你对该项目有改进建议或发现 Bug，欢迎提交 Issue 或 Pull Request！

1. **Fork 本仓库**
2. **创建你的分支 (**​**​`git checkout -b feature-branch`​**​ **)**
3. **提交修改 (**​**​`git commit -m 'Add new feature'`​**​ **)**
4. **推送 (**​**​`git push origin feature-branch`​**​ **)**
5. **提交 Pull Request**

---

## 许可证 / License

MIT License - 你可以自由使用、修改和分发本项目，但请保留原始版权信息。