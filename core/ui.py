import sys
import threading

import customtkinter as tk

from component.InfoFrame import InfoFrame
from component.MySlider import MySlider
from component.MyText import TextRedirector

# from component.InfoFrame import InfoFrame
from component.OptionGroup import OptionGroup
from utils import FA_OPTION, OPTION, VIDEOSIZE, SLIDER_TEXT


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

        # last record frame
        self.last_frame = tk.CTkLabel(
            master=self, text="", width=1000, height=1, anchor="w"
        )
        self.last_frame.place(x=650, y=8)

        # 视频显示界面
        self.video_frames = tk.CTkLabel(
            master=self, text="", width=VIDEOSIZE[0], height=VIDEOSIZE[1]
        )
        self.video_frames.place(x=50, y=50, anchor="nw")

        # Mode Switch
        self.mode = tk.IntVar(value=0)
        self.mode_switch = tk.CTkSwitch(
            master=self,
            variable=self.mode,
            text="preview mode",
            command=self.master.mode_switch,
            state="disabled",
        )
        self.mode_switch.place(x=50, y=550)

        # 加载上一个视频片段按钮
        self.load_button_prev = tk.CTkButton(
            master=self,
            text="Load prev(l)",
            command=self.master.step_backward,
            state="disabled",
        )
        self.load_button_prev.place(x=200, y=550)

        # 加载下一个视频片段按钮
        self.load_button_next = tk.CTkButton(
            master=self,
            text="Load next(n)",
            command=self.master.step_forward,
            state="disabled",
        )
        self.load_button_next.place(x=350, y=550)

        # 重新播放视频片段按钮
        self.reload_button = tk.CTkButton(
            master=self,
            text="Reload",
            command=self.master.reload_video,
            state="disabled",
        )
        self.reload_button.place(x=500, y=550)

        # 保存按钮
        self.save_button = tk.CTkButton(
            master=self,
            text="Save(Enter)",
            command=lambda: threading.Thread(target=self.master.save_segment).start(),
            state="disabled",
        )
        self.save_button.place(x=650, y=550)

        # playtime 调整
        self.playtime_label = tk.CTkLabel(text="间隔步长/s:", master=self)
        self.playtime_label.place(x=1000, y=50)
        self.playtime = tk.DoubleVar()
        self.playtime.set(3)
        self.playtime_enter = tk.CTkEntry(
            master=self,
            width=40,
            textvariable=self.playtime,
        )
        self.playtime_enter.place(x=1100, y=50)
        # save video or not
        self.save = tk.IntVar(value=0)
        self.check = tk.CTkCheckBox(master=self, text="Save video", variable=self.save)
        self.check.place(x=1000, y=120)

        # emotion option

        self.emo_option = OptionGroup(
            master=self, option=OPTION, default=2, state="normal"
        )
        self.emo_option.place(x=800, y=50)

        # potency and arousal option
        self.num_slider = [
            MySlider(master=self, text=key, default=item, state="disabled")
            for key, item in SLIDER_TEXT.items()
        ]
        self.num_slider[0].place(x=800, y=200)
        self.num_slider[1].place(x=800, y=280)

        # fatigue option
        self.fatigue_option = OptionGroup(
            master=self, option=FA_OPTION, default=1, state="normal"
        )
        self.fatigue_option.place(x=800, y=380)
        self.video_info = InfoFrame(master=self)
        self.video_info.place(x=930, y=380, anchor="nw")

        # output text
        self.text = tk.CTkTextbox(master=self, width=900, height=250)
        self.text.place(x=50, y=600, anchor="nw")
        sys.stdout = TextRedirector(self.text, "stdout")
        # print("for test")

        # file count
        self.file_count_label = tk.CTkLabel(master=self, text="File count")
        self.file_count_label.place(x=1040, y=650)
        self.file_count_num = tk.CTkLabel(
            master=self, text=str(self.master.file_count), font=("", 30)
        )
        self.file_count_num.place(x=1060, y=700)

        # reset file count button
        self.rest_file_count_button = tk.CTkButton(
            master=self, text="reset", command=self.master.reset_file_count
        )
        self.rest_file_count_button.place(x=1000, y=750)

    def update_button_status(self, app):
        if getattr(app, "video", None):
            for i in (
                # self.load_button_next,
                # self.load_button_prev,
                self.reload_button,
                self.save_button,
                self.num_slider[0].slider,
                self.num_slider[1].slider,
                self.mode_switch,
            ):
                i.configure(state="normal")
