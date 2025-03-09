import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import sys
import datetime

#达芬奇官方函数
def load_source(module_name, file_path):
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 5:
        import importlib.util

        module = None
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec:
            module = importlib.util.module_from_spec(spec)
        if module:
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        return module
    else:
        import imp
        return imp.load_source(module_name, file_path)

#达芬奇官方函数
def GetResolve():
    try:
        # The PYTHONPATH needs to be set correctly for this import statement to work.
        # An alternative is to import the DaVinciResolveScript by specifying absolute path (see ExceptionHandler logic)
        import DaVinciResolveScript as bmd
    except ImportError:
        if sys.platform.startswith("darwin"):
            expectedPath = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            import os
            expectedPath = os.getenv('PROGRAMDATA') + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
        elif sys.platform.startswith("linux"):
            expectedPath = "/opt/resolve/Developer/Scripting/Modules/"

        # check if the default path has it...
        # print("Unable to find module DaVinciResolveScript from $PYTHONPATH - trying default locations")
        try:
            load_source('DaVinciResolveScript', expectedPath + "DaVinciResolveScript.py")
            import DaVinciResolveScript as bmd
        except Exception as ex:
            # No fallbacks ... report error:
            print("Unable to find module DaVinciResolveScript - please ensure that the module DaVinciResolveScript is discoverable by python")
            print("For a default DaVinci Resolve installation, the module is expected to be located in: " + expectedPath)
            print(ex)
            sys.exit()

    return bmd.scriptapp("Resolve")

#按钮功能
#def button0_clicked():
#    test()

def button1_clicked():
    timeline_delete_disabled_audio_clips()

def button2_clicked():
    timeline_delete_disabled_video_clips()

def button3_clicked():
    timeline_delete_enabled_audio_clips()

def button4_clicked():
    timeline_delete_enabled_video_clips()

def button5_clicked():
    timeline_delete_offline_video_clips()

def button6_clicked():
    timeline_delete_offline_audio_clips()

def button7_clicked():
    timeline_toggle_video_clips_enabled()

def button8_clicked():
    timeline_toggle_audio_clips_enabled()

# 创建主窗口
window = tk.Tk()
window.title("HZK达芬奇剪辑脚本")
window.geometry("400x500")
window.resizable(False, False)

# 创建标签
label = tk.Label(window, text="")
label.pack(pady=5)
label.config(text="请选择要执行的脚本")

# 创建按钮
# button0 = tk.Button(window, text="测试", command=button0_clicked)
# button0.pack(pady=5)

button1 = tk.Button(window, text="时间线_删除未启用音频", command=button1_clicked)
button1.pack(pady=5)

button2 = tk.Button(window, text="时间线_删除未启用视频", command=button2_clicked)
button2.pack(pady=5)

button3 = tk.Button(window, text="时间线_删除启用音频", command=button3_clicked)
button3.pack(pady=5)

button4 = tk.Button(window, text="时间线_删除启用视频", command=button4_clicked)
button4.pack(pady=5)

button5 = tk.Button(window, text="时间线_删除离线视频", command=button5_clicked)
button5.pack(pady=5)

button6 = tk.Button(window, text="时间线_删除离线音频", command=button6_clicked)
button6.pack(pady=5)

button7 = tk.Button(window, text="时间线_切换视频启用状态", command=button7_clicked)
button7.pack(pady=5)

button8 = tk.Button(window, text="时间线_切换音频启用状态", command=button8_clicked)
button8.pack(pady=5)

# 创建控制台
console_output = scrolledtext.ScrolledText(window, height=15, width=50, wrap=tk.WORD)
console_output.pack(pady=10)
console_output.config(state=tk.DISABLED, bg="lightgray", fg="black")

# 函数用于向控制台输出内容
def insert_to_console(message):
    console_output.config(state=tk.NORMAL)  # 允许写入内容
    # 插入消息并自动滚动到底部
    console_output.insert(tk.END, message + "\n")  # 每条消息自动换行
    console_output.see(tk.END)  # 自动滚动到最新消息

# 获取时间
# insert_to_console(f"【{get_current_time()}】 没有未启用音频！")
def get_current_time():
    """
    返回当前时间的字符串，格式为 HH:mm:ss
    """
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 格式化时间为 HH:mm:ss
    return current_time.strftime("%H:%M:%S")

#测试按钮
def test():
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【测试】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【测试】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的音频轨道
    track_count = timeline.GetTrackCount("video")
    if track_count == 0:
        insert_to_console("【测试】 时间线上没有视频轨道。")
        return
    
    # 遍历所有音频轨道和片段
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("video", track_index)
        
        if not clips:
            insert_to_console(f"【测试】 视频轨道 {track_index} 没有片段。")
            continue
        print(clips[0].GetMediaPoolItem().GetClipProperty())

#时间线_删除未启用音频
def timeline_delete_disabled_audio_clips():
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【时间线_删除未启用音频】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【时间线_删除未启用音频】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的音频轨道
    track_count = timeline.GetTrackCount("audio")
    if track_count == 0:
        insert_to_console("【时间线_删除未启用音频】 时间线上没有音频轨道。")
        return
    
    insert_to_console(f"【时间线_删除未启用音频】 检测到 {track_count} 条音频轨道。")
    
    # 遍历所有音频轨道和片段
    disabled_clips = []
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("audio", track_index)
        
        if not clips:
            insert_to_console(f"【时间线_删除未启用音频】 音频轨道 {track_index} 没有片段。")
            continue
        
        for clip in clips:
            if clip is None:
                insert_to_console(f"【时间线_删除未启用音频】 跳过无效片段（轨道 {track_index}）。")
                continue
            
            # 检查片段是否未启用
            enabled = clip.GetClipEnabled()
            # print(clip.GetName())
            # print(enabled)
            if enabled is None:
                insert_to_console(f"【时间线_删除未启用音频】 无法获取片段属性（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            if not enabled:
                # 选中未启用的片段
                disabled_clips.append(clip)
                # print("正在删除片段",clip.GetName(),timeline.DeleteClips(clip, False))
    # 统一删除所有未启用的片段
    if disabled_clips:
        response = messagebox.askokcancel("提示", f"即将删除 {len(disabled_clips)} 个未启用的片段...")
        if response:
            result = timeline.DeleteClips(disabled_clips, False)
            if response:
                insert_to_console("【时间线_删除未启用音频】 删除成功！")
            else:
                insert_to_console("【时间线_删除未启用音频】 删除失败！")
            
        else:
            insert_to_console("【时间线_删除未启用音频】 已取消！")
    else:
        insert_to_console("【时间线_删除未启用音频】 没有未启用音频！")

#时间线_删除未启用视频
def timeline_delete_disabled_video_clips():
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【时间线_删除未启用视频】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【时间线_删除未启用视频】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的视频轨道
    track_count = timeline.GetTrackCount("video")
    if track_count == 0:
        insert_to_console("【时间线_删除未启用视频】 时间线上没有视频轨道。")
        return
    
    insert_to_console(f"【时间线_删除未启用视频】 检测到 {track_count} 条视频轨道。")
    
    # 遍历所有视频轨道和片段
    disabled_clips = []
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("video", track_index)
        
        if not clips:
            insert_to_console(f"【时间线_删除未启用视频】 视频轨道 {track_index} 没有片段。")
            continue
        
        for clip in clips:
            if clip is None:
                insert_to_console(f"【时间线_删除未启用视频】 跳过无效片段（轨道 {track_index}）。")
                continue
            
            # 检查片段是否未启用
            enabled = clip.GetClipEnabled()
            if enabled is None:
                insert_to_console(f"【时间线_删除未启用视频】 无法获取片段属性（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            if not enabled:
                # 选中未启用的片段
                disabled_clips.append(clip)
    
    # 统一删除所有未启用的片段
    if disabled_clips:
        response = messagebox.askokcancel("提示", f"即将删除 {len(disabled_clips)} 个未启用的视频片段...")
        if response:
            result = timeline.DeleteClips(disabled_clips, False)
            if result:
                insert_to_console("【时间线_删除未启用视频】 删除成功！")
            else:
                insert_to_console("【时间线_删除未启用视频】 删除失败！")
        else:
            insert_to_console("【时间线_删除未启用视频】 已取消！")
    else:
        insert_to_console("【时间线_删除未启用视频】 没有未启用视频！")

#时间线_删除启用视频
def timeline_delete_enabled_video_clips():
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【时间线_删除启用视频】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【时间线_删除启用视频】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的视频轨道
    track_count = timeline.GetTrackCount("video")
    if track_count == 0:
        insert_to_console("【时间线_删除启用视频】 时间线上没有视频轨道。")
        return
    
    insert_to_console(f"【时间线_删除启用视频】 检测到 {track_count} 条视频轨道。")
    
    # 遍历所有视频轨道和片段
    enabled_clips = []
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("video", track_index)
        
        if not clips:
            insert_to_console(f"【时间线_删除启用视频】 视频轨道 {track_index} 没有片段。")
            continue
        
        for clip in clips:
            if clip is None:
                insert_to_console(f"【时间线_删除启用视频】 跳过无效片段（轨道 {track_index}）。")
                continue
            
            # 检查片段是否启用
            enabled = clip.GetClipEnabled()
            if enabled is None:
                insert_to_console(f"【时间线_删除启用视频】 无法获取片段属性（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            if enabled:
                # 选中启用的片段
                enabled_clips.append(clip)
    
    # 统一删除所有启用的片段
    if enabled_clips:
        response = messagebox.askokcancel("提示", f"即将删除 {len(enabled_clips)} 个启用的视频片段...")
        if response:
            result = timeline.DeleteClips(enabled_clips, False)
            if result:
                insert_to_console("【时间线_删除启用视频】 删除成功！")
            else:
                insert_to_console("【时间线_删除启用视频】 删除失败！")
        else:
            insert_to_console("【时间线_删除启用视频】 已取消！")
    else:
        insert_to_console("【时间线_删除启用视频】 没有启用的视频！")

#时间线_删除启用音频
def timeline_delete_enabled_audio_clips():
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【时间线_删除启用音频】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【时间线_删除启用音频】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的音频轨道
    track_count = timeline.GetTrackCount("audio")
    if track_count == 0:
        insert_to_console("【时间线_删除启用音频】 时间线上没有音频轨道。")
        return
    
    insert_to_console(f"【时间线_删除启用音频】 检测到 {track_count} 条音频轨道。")
    
    # 遍历所有音频轨道和片段
    enabled_clips = []
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("audio", track_index)
        
        if not clips:
            insert_to_console(f"【时间线_删除启用音频】 音频轨道 {track_index} 没有片段。")
            continue
        
        for clip in clips:
            if clip is None:
                insert_to_console(f"【时间线_删除启用音频】 跳过无效片段（轨道 {track_index}）。")
                continue
            
            # 检查片段是否启用
            enabled = clip.GetClipEnabled()
            if enabled is None:
                insert_to_console(f"【时间线_删除启用音频】 无法获取片段属性（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            if enabled:
                # 选中启用的片段
                enabled_clips.append(clip)
    
    # 统一删除所有启用的片段
    if enabled_clips:
        response = messagebox.askokcancel("提示", f"即将删除 {len(enabled_clips)} 个启用的音频片段...")
        if response:
            result = timeline.DeleteClips(enabled_clips, False)
            if result:
                insert_to_console("【时间线_删除启用音频】 删除成功！")
            else:
                insert_to_console("【时间线_删除启用音频】 删除失败！")
        else:
            insert_to_console("【时间线_删除启用音频】 已取消！")
    else:
        insert_to_console("【时间线_删除启用音频】 没有启用的音频！")

#时间线_删除离线视频
def timeline_delete_offline_video_clips():
    # 获取 DaVinci Resolve 的对象
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【时间线_删除离线视频】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【时间线_删除离线视频】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的视频轨道
    track_count = timeline.GetTrackCount("video")
    if track_count == 0:
        insert_to_console("【时间线_删除离线视频】 时间线上没有视频轨道。")
        return
    
    insert_to_console(f"【时间线_删除离线视频】 检测到 {track_count} 条视频轨道。")
    
    # 遍历所有视频轨道和片段
    offline_clips = []
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("video", track_index)
        
        if not clips:
            insert_to_console(f"【时间线_删除离线视频】 视频轨道 {track_index} 没有片段。")
            continue
        
        for clip in clips:
            if clip is None:
                insert_to_console(f"【时间线_删除离线视频】 跳过无效片段（轨道 {track_index}）。")
                continue
            
            # 获取片段的 MediaPoolItem
            media_pool_item = clip.GetMediaPoolItem()
            if not media_pool_item:
                insert_to_console(f"【时间线_删除离线视频】 无法获取 MediaPoolItem（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            # 检查片段的在线状态
            clip_properties = media_pool_item.GetClipProperty()
            if not clip_properties:
                insert_to_console(f"【时间线_删除离线视频】 无法获取片段属性（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            online_status = clip_properties.get("Online Status")
            if online_status == "Offline":
                insert_to_console(f"【时间线_删除离线视频】 检测到离线片段：{clip.GetName()}（轨道 {track_index}）。")
                offline_clips.append(clip)
    
    # 删除所有离线片段
    if offline_clips:
        response = messagebox.askokcancel("提示", f"即将删除 {len(offline_clips)} 个离线片段...")
        if response:
            result = timeline.DeleteClips(offline_clips, False)
            if result:
                insert_to_console("【时间线_删除离线片段】 删除成功！")
            else:
                insert_to_console("【时间线_删除离线片段】 删除失败！")
        else:
            insert_to_console("【时间线_删除离线片段】 已取消！")
    else:
        insert_to_console("【时间线_删除离线片段】 没有检测到离线片段。")

# 时间线_删除离线音频
def timeline_delete_offline_audio_clips():
    # 获取 DaVinci Resolve 的对象
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【时间线_删除离线音频】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【时间线_删除离线音频】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的音频轨道
    track_count = timeline.GetTrackCount("audio")
    if track_count == 0:
        insert_to_console("【时间线_删除离线音频】 时间线上没有音频轨道。")
        return
    
    insert_to_console(f"【时间线_删除离线音频】 检测到 {track_count} 条音频轨道。")
    
    # 遍历所有音频轨道和片段
    offline_clips = []
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("audio", track_index)
        
        if not clips:
            insert_to_console(f"【时间线_删除离线音频】 音频轨道 {track_index} 没有片段。")
            continue
        
        for clip in clips:
            if clip is None:
                insert_to_console(f"【时间线_删除离线音频】 跳过无效片段（轨道 {track_index}）。")
                continue
            
            # 获取片段的 MediaPoolItem
            media_pool_item = clip.GetMediaPoolItem()
            if not media_pool_item:
                insert_to_console(f"【时间线_删除离线音频】 无法获取 MediaPoolItem（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            # 检查片段的在线状态
            clip_properties = media_pool_item.GetClipProperty()
            if not clip_properties:
                insert_to_console(f"【时间线_删除离线音频】 无法获取片段属性（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            online_status = clip_properties.get("Online Status")
            if online_status == "Offline":
                insert_to_console(f"【时间线_删除离线音频】 检测到离线片段：{clip.GetName()}（轨道 {track_index}）。")
                offline_clips.append(clip)
    
    # 删除所有离线片段
    if offline_clips:
        response = messagebox.askokcancel("提示", f"即将删除 {len(offline_clips)} 个离线片段...")
        if response:
            result = timeline.DeleteClips(offline_clips, False)
            if result:
                insert_to_console("【时间线_删除离线音频】 删除成功！")
            else:
                insert_to_console("【时间线_删除离线音频】 删除失败！")
        else:
            insert_to_console("【时间线_删除离线音频】 已取消！")
    else:
        insert_to_console("【时间线_删除离线音频】 没有检测到离线片段。")

# 时间线_切换视频启用状态
def timeline_toggle_video_clips_enabled():
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【时间线_切换视频启用状态】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【时间线_切换视频启用状态】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的视频轨道
    track_count = timeline.GetTrackCount("video")
    if track_count == 0:
        insert_to_console("【时间线_切换视频启用状态】 时间线上没有视频轨道。")
        return
    
    insert_to_console(f"【时间线_切换视频启用状态】 检测到 {track_count} 条视频轨道。")
    
    toggled_clips = 0  # 记录切换的片段数量
    
    # 遍历所有视频轨道和片段
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("video", track_index)
        
        if not clips:
            insert_to_console(f"【时间线_切换视频启用状态】 视频轨道 {track_index} 没有片段。")
            continue
        
        for clip in clips:
            if clip is None:
                insert_to_console(f"【时间线_切换视频启用状态】 跳过无效片段（轨道 {track_index}）。")
                continue
            
            # 获取当前片段的启用状态
            enabled = clip.GetClipEnabled()
            if enabled is None:
                insert_to_console(f"【时间线_切换视频启用状态】 无法获取片段属性（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            # 切换启用状态
            new_state = not enabled
            result = clip.SetClipEnabled(new_state)
            
            if result:
                status = "启用" if new_state else "禁用"
                insert_to_console(f"【时间线_切换视频启用状态】 片段 {clip.GetName()} 已{status}。")
                toggled_clips += 1
            else:
                insert_to_console(f"【时间线_切换视频启用状态】 片段 {clip.GetName()} 状态切换失败。")
    
    if toggled_clips == 0:
        insert_to_console("【时间线_切换视频启用状态】 没有可切换状态的视频片段。")
    else:
        insert_to_console(f"【时间线_切换视频启用状态】 共切换 {toggled_clips} 个视频片段的启用状态。")

# 时间线_切换音频启用状态
def timeline_toggle_audio_clips_enabled():
    resolve = GetResolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    if not project:
        insert_to_console("【时间线_切换音频启用状态】 没有打开的项目，请先打开一个项目！")
        return
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        insert_to_console("【时间线_切换音频启用状态】 没有打开的时间线，请先打开一个时间线。")
        return
    
    # 获取所有的音频轨道
    track_count = timeline.GetTrackCount("audio")
    if track_count == 0:
        insert_to_console("【时间线_切换音频启用状态】 时间线上没有音频轨道。")
        return
    
    insert_to_console(f"【时间线_切换音频启用状态】 检测到 {track_count} 条音频轨道。")
    
    toggled_clips = 0  # 记录切换的片段数量
    
    # 遍历所有音频轨道和片段
    for track_index in range(1, track_count + 1):
        clips = timeline.GetItemListInTrack("audio", track_index)
        
        if not clips:
            insert_to_console(f"【时间线_切换音频启用状态】 音频轨道 {track_index} 没有片段。")
            continue
        
        for clip in clips:
            if clip is None:
                insert_to_console(f"【时间线_切换音频启用状态】 跳过无效片段（轨道 {track_index}）。")
                continue
            
            # 获取当前片段的启用状态
            enabled = clip.GetClipEnabled()
            if enabled is None:
                insert_to_console(f"【时间线_切换音频启用状态】 无法获取片段属性（轨道 {track_index}，片段 {clip.GetName()}）。")
                continue
            
            # 切换启用状态
            new_state = not enabled
            result = clip.SetClipEnabled(new_state)
            
            if result:
                status = "启用" if new_state else "禁用"
                insert_to_console(f"【时间线_切换音频启用状态】 片段 {clip.GetName()} 已{status}。")
                toggled_clips += 1
            else:
                insert_to_console(f"【时间线_切换音频启用状态】 片段 {clip.GetName()} 状态切换失败。")
    
    if toggled_clips == 0:
        insert_to_console("【时间线_切换音频启用状态】 没有可切换状态的音频片段。")
    else:
        insert_to_console(f"【时间线_切换音频启用状态】 共切换 {toggled_clips} 个音频片段的启用状态。")


# 运行主循环
window.mainloop()