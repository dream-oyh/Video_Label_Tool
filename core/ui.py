import tkinter as tk

# from component.InfoFrame import InfoFrame
from component.OptionGroup import OptionGroup
from core.Video import play_video, save_video
from utils import next_segment, open_video, prev_segment


class MyFrame(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 打开文件按钮
        self.file_open_button = tk.Button(
            master=self,
            text="打开文件",
            command=lambda: open_video(app=self.master),
        )
        self.file_open_button.place(x=0, y=0)
        # 标签选项设置
        self.option = ["Anger", "Happy", "Sad", "Anxious"]
        # 显示打开文件路径，确保文件正确读取
        self.video_path_label = tk.Label(
            master=self, text="", width=1000, height=1, anchor="w"
        )
        self.video_path_label.place(x=80, y=0)
        # 视频显示界面
        self.video_frames = tk.Label(
            master=self, text="", width=650, height=360
        )  # , width=540, height=360
        self.video_frames.place(x=0, y=50)

        # 加载上一个视频片段
        self.load_button_prev = tk.Button(
            master=self,
            text="Load prev",
            command=lambda: prev_segment(app=self.master),
        )
        self.load_button_prev.place(x=200, y=450)

        # 加载下一个视频片段
        self.load_button_next = tk.Button(
            master=self,
            text="Load next",
            command=lambda: next_segment(app=self.master),
        )
        self.load_button_next.place(x=350, y=450)

        # 重新播放视频片段
        self.reload_button = tk.Button(
            master=self,
            text="Reload",
            command=lambda: play_video(app=self.master),
        )
        self.reload_button.place(x=500, y=450)

        # playtime 调整
        self.playtime_label = tk.Label(text="间隔步长/s:", master=self)
        self.playtime_label.place(x=80, y=450)
        self.playtime = tk.DoubleVar()
        self.playtime.set(3)
        self.playtime_enter = tk.Entry(
            master=self,
            width=10,
            textvariable=self.playtime,
        )
        self.playtime_enter.place(x=80, y=480)

        # 标签选项设置

        self.label_option = OptionGroup(option=self.option)
        self.label_option.place(x=650, y=100)

        # 保存按钮
        # self.save_button = tk.Button(
        #     master=self, text="Save", command=lambda: save_label(app=self.master)
        # )
        self.save_button = tk.Button(
            master=self,
            text="Save",
            command=lambda: save_video(app=self.master),
        )
        self.save_button.place(x=650, y=450)

    # def view_info(self):
    #     # 显示导入视频信息
    #     self.video_info = InfoFrame(master=self)
    #     self.video_info.place(x=0, y=0)
