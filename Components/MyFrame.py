import tkinter as tk
from .FileOpenButton import FileOpenButton
from .LoadButton import LoadButton
from .ReLoadButton import ReLoadButton
from .LastLoadButton import LastLoadButton


class MyFrame(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 打开文件按钮
        self.file_open_button = FileOpenButton(master=self, text="Open File")
        self.file_open_button.place(x=0, y=0)
        # 显示打开文件路径，确保文件正确读取
        self.video_path_label = tk.Label(
            master=self, text="", width=1000, height=1, anchor="w"
        )
        self.video_path_label.place(x=80, y=0)
        # 视频显示界面
        self.video_frames = tk.Label(
            master=self, text="Video", width=650, height=360
        )  # , width=540, height=360
        self.video_frames.place(x=0, y=50)

        # 加载下一个视频按钮
        self.load_button = LoadButton(master=self, text="Load next")
        self.load_button.place(x=300, y=450)

        # 加载上一个视频按钮
        self.load_button = LastLoadButton(master=self, text="Load last")
        self.load_button.place(x=150, y=450)

        # 重新播放按钮
        self.reload_button = ReLoadButton(master=self, text="Reload")
        self.reload_button.place(x=450, y=450)
