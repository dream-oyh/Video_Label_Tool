import tkinter as tk

from core.PlayVideo import play_video
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
        self.load_button_prev.place(x=150, y=450)

        # 加载下一个视频片段
        self.load_button_next = tk.Button(
            master=self,
            text="Load next",
            command=lambda: next_segment(app=self.master),
        )
        self.load_button_next.place(x=300, y=450)

        # 重新播放视频片段
        self.reload_button = tk.Button(
            master=self,
            text="Reload",
            command=lambda: play_video(app=self.master),
        )
        self.reload_button.place(x=450, y=450)
