import threading

import customtkinter as tk

from component.InfoFrame import InfoFrame

# from component.InfoFrame import InfoFrame
from component.OptionGroup import OptionGroup
from utils import OPTION, VIDEOSIZE


class MyFrame(tk.CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 打开文件按钮
        self.file_open_button = tk.CTkButton(
            master=self, text="打开文件", command=self.master.open_video
        )
        self.file_open_button.place(x=0, y=0)

        # 显示打开文件路径，确保文件正确读取
        self.video_path_label = tk.CTkLabel(
            master=self, text="", width=1000, height=1, anchor="w"
        )
        self.video_path_label.place(x=170, y=8)

        # 视频显示界面
        self.video_frames = tk.CTkLabel(
            master=self, text="", width=VIDEOSIZE[0], height=VIDEOSIZE[1]
        )
        self.video_frames.place(x=0, y=50, anchor="nw")

        # 加载上一个视频片段按钮
        self.load_button_prev = tk.CTkButton(
            master=self,
            text="Load prev",
            command=self.master.step_backward,
            state="disabled",
        )
        self.load_button_prev.place(x=200, y=550)

        # 加载下一个视频片段按钮
        self.load_button_next = tk.CTkButton(
            master=self,
            text="Load next",
            command=self.master.step_forward,
            state="disabled",
        )
        self.load_button_next.place(x=350, y=550)

        # 重新播放视频片段按钮
        self.reload_button = tk.CTkButton(
            master=self,
            text="Reload",
            command=self.master.play_video,
            state="disabled",
        )
        self.reload_button.place(x=500, y=550)

        # 保存按钮
        self.save_button = tk.CTkButton(
            master=self,
            text="Save",
            command=lambda: threading.Thread(target=self.master.save_segment).start(),
            state="disabled",
        )
        self.save_button.place(x=650, y=550)

        # playtime 调整
        self.playtime_label = tk.CTkLabel(text="间隔步长/s:", master=self)
        self.playtime_label.place(x=80, y=550)
        self.playtime = tk.DoubleVar()
        self.playtime.set(3)
        self.playtime_enter = tk.CTkEntry(
            master=self,
            width=40,
            textvariable=self.playtime,
        )
        self.playtime_enter.place(x=80, y=580)

        # 标签选项设置

        self.label_option = OptionGroup(master=self, option=OPTION)
        self.label_option.place(x=800, y=100)

        self.video_info = InfoFrame(master=self)
        self.video_info.place(x=800, y=200, anchor="nw")

    def update_button_status(self, app):
        if getattr(app, "video", None):
            for i in (
                self.load_button_next,
                self.load_button_prev,
                self.reload_button,
                self.save_button,
            ):
                i.configure(state="normal")
