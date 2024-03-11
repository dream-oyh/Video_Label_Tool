import csv
import logging
import os
import sys
import threading
from contextlib import suppress
from pathlib import Path
from tkinter import filedialog

import customtkinter as tk
import cv2
import pandas
import pandas as pd
from PIL import Image

from component.MyText import TextRedirector
from core.ui import MyFrame
from utils import FA_OPTION, OPTION, VIDEOSIZE

# output_path = Path("output")
# output_path.mkdir(exist_ok=True)


class VideoFrameError(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)


class APP(tk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_count = 0  # 打开文件个数
        self.frame = MyFrame(master=self, width=1200, height=900)
        self.frame.grid(row=1, column=1, padx=250, pady=50)
        self.video: cv2.VideoCapture  # 视频
        self.cut_point = 0  # 当前切割点
        self.image: tk.CTkImage
        self.frame.file_count_num.configure(text=str(self.file_count))
        if not os.path.exists(".cache"):
            os.makedirs(".cache", exist_ok=True)
            with open(".cache/last_open.txt", "w", newline="") as f:
                f.write("")
        with open(".cache/last_open.txt", "r") as f:
            try:
                self.last_open = f.readlines()[-1]
            except:
                self.frame.video_path_label.configure(text="请选择你的第一个视频文件")
                self.last_open = "0"
            else:
                self.frame.video_path_label.configure(
                    text="您上次打开的文件是：" + str(self.last_open)
                )

    @property
    def fps(self) -> float:
        """
        视频帧率
        """
        return self.video.get(cv2.CAP_PROP_FPS)

    @property
    def frame_count(self) -> float:
        """
        视频总帧数
        """
        return self.video.get(cv2.CAP_PROP_FRAME_COUNT)

    @property
    def get_total_time(self) -> float:
        """
        视频总时间
        """
        return self.frame_count / self.fps

    @property
    def current_time(self) -> float:
        """
        当前播放时间
        """
        return self.cut_point / self.fps

    @property
    def play_step_sec(self) -> int:
        """
        获取播放步长（秒）
        """
        return self.frame.playtime.get()

    @property
    def play_step_frame(self) -> int:
        """
        获取播放步长（帧）
        """
        return round(self.play_step_sec * self.fps)

    @property
    def video_frame(self) -> int:
        """
        获取视频当前帧
        """
        return self.video.get(cv2.CAP_PROP_POS_FRAMES)

    @property
    def segment_end(self) -> int:
        """
        获取当前分段的右端点（帧）
        """
        return self.cut_point + self.play_step_frame

    def update_frame_pos(self):
        """
        更新视频帧位置至当前切割点
        """
        self.video.set(cv2.CAP_PROP_POS_FRAMES, round(self.cut_point))

    def move_cursor(self, bias: int) -> int:
        """
        移动当前切割点
        :param bias: 偏移量
        :returns: 该点的新位置
        """
        temp = self.cut_point + bias
        if temp <= self.frame_count and temp >= 0:
            self.cut_point = temp
        logging.info(f"当前帧：{self.cut_point}，当前时间：{self.current_time}")
        return self.cut_point

    def step_forward(self):
        """
        向后移动一步 cursor，并播放视频片段
        """
        self.set_bind("l")
        if self.cut_point + self.play_step_frame > self.frame_count:
            self.redirectPrint(
                "[ERROR] The video is over, you can't get next clip ! Please open next video file."
            )
            self.unbind(["E", "n"])
        else:
            self.redirectPrint(
                "The video cut point has stepped forward to "
                + str(self.cut_point + self.play_step_frame)
                + "th frame"
            )
            if self.frame.mode_switch.get() == 0:
                self.set_bind("E")
                self.set_unbind("n")
            # self.set_bind("E")
            # if self.frame.mode_switch.get() == 1:
            #     self.set_unbind("n")
            self.move_cursor(self.play_step_frame)
            self.update_frame_pos()
            self.frame.video_info.update_info()
            self.play_video()

    def step_backward(self):
        """
        向前移动一步 cursor，并播放视频片段
        """
        if self.cut_point >= self.play_step_frame:
            self.redirectPrint(
                "The video cut point has stepped backward to "
                + str(self.cut_point - self.play_step_frame)
                + "th frame"
            )
            if (
                self.frame.save_button.cget("state") == "normal"
                and self.frame.mode_switch.get() == 0
            ):
                self.redirectPrint(
                    "[LOADING] The last record is deleting. Please loading ......"
                )
                self.delete_record(self.csv_path, 1)
                self.redirectPrint(
                    "You have deleted the last record. Now you can re-record this clip label."
                )
            if (
                self.frame.save_button.cget("state") == "disabled"
                and self.frame.mode_switch.get() == 0
            ):
                self.redirectPrint(
                    "[LOADING] The last record is deleting. Please loading ......"
                )
                self.delete_record(self.csv_path, 2)
                self.redirectPrint(
                    "You have deleted the last record. Now you can re-record this clip label."
                )
                self.redirectPrint(
                    "[WARNING] Because of you have added a new label, so this label will be deleted as well. You need to re-record it again."
                )
            if self.frame.mode_switch.get() == 0:
                self.set_bind("E")
                self.set_unbind("n")
            self.move_cursor(-self.play_step_frame)
            self.update_frame_pos()
            self.frame.video_info.update_info()
            self.play_video()
        else:
            self.redirectPrint("[ERROR] You have arrived the head of this video! ")
            self.set_unbind("l")

    def open_video(self):
        """
        打开视频文件
        """
        self.file_path = filedialog.askopenfilename()
        self.frame.load_button_next.configure(state="disabled")
        self.frame.load_button_prev.configure(state="disabled")
        if str(self.last_open.rstrip()) != str(self.file_path):
            with open(".cache/last_open.txt", "a+") as f:
                f.write(self.file_path)
                f.write("\n")
        self.f_path, self.file_name = os.path.split(self.file_path)
        self.redirectPrint(
            "You have opened the video! The video name is:\n" + self.file_name
        )
        with open(".cache/last_open.txt", "r") as f:
            count = len(f.readlines())
        self.file_count = count
        self.frame.file_count_num.configure(text=str(self.file_count))
        logging.info("Opening video file: " + self.file_path)
        self.set_bind(["E", "n"])
        self.frame.video_path_label.configure(text=self.file_path)
        self.video = cv2.VideoCapture(self.file_path)
        assert self.video.isOpened(), "Video is not opened"
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEOSIZE[0])
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEOSIZE[1])
        self.cut_point = 0
        self.redirectPrint(
            f"视频帧率：{self.fps}\n视频总帧数：{self.frame_count}\n视频总时间：{self.get_total_time}\n"
        )
        self.frame.video_info.update_info()
        self.frame.update_button_status(self)
        self.init_csv()
        self.play_video()

    def play_video(self):
        """
        播放一个视频片段
        """
        self.update_frame_pos()
        while self.video_frame <= self.cut_point + self.play_step_frame:
            with suppress(VideoFrameError):
                self.show_next_frame()

    def reload_video(self):
        self.redirectPrint("This video clip has reloaded.\n")
        self.play_video()

    def show_next_frame(self):
        """
        读取当前帧并显示
        :raise
        """
        for _ in range(2):
            ret = self.video.grab()
            if not ret:
                raise VideoFrameError("Cannot get video frame")
        _, readyframe = self.video.retrieve()
        if readyframe is None:
            raise VideoFrameError("Cannot get video frame")

        frame = cv2.cvtColor(readyframe, cv2.COLOR_BGR2RGBA)  # 转至 RGB 色彩空间
        # frame = cv2.resize(frame, dsize=(20, 80))
        self.image = tk.CTkImage(Image.fromarray(frame), size=VIDEOSIZE)
        self.frame.video_frames.configure(image=self.image)
        self.frame.video_frames.update()

    def save_segment(self):
        """
        保存视频片段，在 csv 中记录标签
        """
        self.redirectPrint("This video clip has saved.")
        self.frame.save_button.configure(state="disabled")
        self.set_unbind("E")
        self.set_bind("n")
        self.write_label()
        if self.frame.check.get():
            option_num: int = self.frame.emo_option.num.get()
            emotion = OPTION[option_num]
            output_path = Path("output")
            output_path.mkdir(exist_ok=True)
            output_path_sub = self.f_path / output_path / emotion
            # print(output_path_sub)
            os.makedirs(output_path_sub, exist_ok=True)
            # output_path_sub.mkdir(exist_ok=True)
            video_index: int = len(list(output_path_sub.glob("*"))) + 1
            self.write_segment(
                output_path_sub
                / (
                    "_".join(
                        (
                            str(video_index),
                            self.emo_label,
                            self.fatigue_label,
                            "potency(" + str(self.potency) + ")",
                            "arousal(" + str(self.arousal) + ")",
                        )
                    )
                    + ".avi"
                )
            )

    def write_segment(self, path: Path):
        """
        将视频片段写入文件
        :param path: 文件路径
        """
        video = self.video
        out = cv2.VideoWriter(
            str(path),
            cv2.VideoWriter_fourcc(*"XVID"),
            25,
            (
                int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            ),
        )

        self.update_frame_pos()
        while self.video_frame <= self.segment_end:
            ret, frame = video.read()
            if not ret or frame is None:
                raise VideoFrameError()
            out.write(frame)

    def init_csv(self):
        """
        初始化 csv 文件
        """
        # f_path, file_name = os.path.split(self.file_path)
        csv_name = self.file_name[0:10]
        header = [
            "start frame",
            "end frame",
            "emotion",
            "potency",
            "arousal",
            "fatigue",
        ]
        # data_init = [-1]
        self.csv_path = str(self.f_path) + "/" + str(csv_name) + ".csv"
        # print(os.path.exists(self.csv_path))
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, mode="w", newline="") as f:
                csv.writer(f).writerow(header)
                # csv.writer(f).writerow(data_init)

    def write_label(self):
        """
        读取并写入用户设置的标签
        """
        self.redirectPrint("Your labels are showed below.")
        frame = self.frame
        emotion_num = frame.emo_option.num.get()
        fatigue_num = frame.fatigue_option.num.get()
        self.emo_label = OPTION[emotion_num]
        self.fatigue_label = FA_OPTION[fatigue_num]
        self.potency = frame.num_slider[0].slider.get()
        self.arousal = frame.num_slider[1].slider.get()
        df = pd.read_csv(self.csv_path)
        try:
            df.tail(1).iloc[0, 0]
        except:
            last_end_frame = 0
        else:
            last_end_frame = df.tail(1).iloc[0, 1]

        label_data = [
            last_end_frame,
            last_end_frame + self.play_step_frame,
            self.emo_label,
            self.potency,
            self.arousal,
            self.fatigue_label,
        ]
        # print(df.tail(1))
        with open(self.csv_path, "a+", newline="") as f:
            csv.writer(f).writerow(label_data)
        df = pd.read_csv(self.csv_path)
        print(df.tail(1))
        print("\n")

    def redirectPrint(self, text):
        """
        print 至输出框
        """
        sys.stdout = TextRedirector(self.frame.text)
        print(text + "\n")

    def reset_file_count(self):
        """
        重置已打开文件数
        """
        with open(".cache/last_open.txt", "w") as f:
            f.write("")
        self.frame.file_count_num.configure(text=0)

    def set_bind(self, keys: list[str]):
        """
        设置快捷键
        :str: 快捷键的值，支持通过列表一次设置多个快捷键
        "E": "Save button"
        "n": "Load next button"
        "l:" "Load prev button"
        """
        for key in keys:
            if key == "E":
                self.bind(
                    "<Return>",
                    lambda event: threading.Thread(target=self.save_segment).start(),
                )
                self.frame.save_button.configure(state="normal")
            elif key == "n":
                self.bind("<Key-n>", lambda _: self.step_forward())
                self.frame.load_button_next.configure(state="normal")
            elif key == "l":
                self.bind("<Key-l>", lambda _: self.step_backward())
                self.frame.load_button_prev.configure(state="normal")

    def set_unbind(self, keys: list[str]):
        """
        取消快捷键
        设置同'set_bind()'
        """
        for key in keys:
            if key == "E":
                self.unbind("<Return>")
                self.frame.save_button.configure(state="disabled")
            elif key == "n":
                self.unbind("<Key-n>")
                self.frame.load_button_next.configure(state="disabled")
            elif key == "l":
                self.unbind("<Key-l>")
                self.frame.load_button_prev.configure(state="disabled")

    def delete_record(self, path, num):
        """
        删除 csv 中存储数据
        :path(str) csv 路径
        :num(int) 删除数据条目
        """
        df = pandas.read_csv(path)
        df.drop(index=df.tail(num).index, axis=0, inplace=True)
        df.to_csv(path, index=None)

    def mode_switch(self):
        if self.frame.mode_switch.get() == 1:
            # in preview mode
            self.set_unbind("E")
            self.redirectPrint("[PREVIEW MODE] You have entered the preview mode!")
        if self.frame.mode_switch.get() == 0:
            # in work space
            self.set_bind("E")
            self.redirectPrint("[WORK MODE] You have entered the work mode!")
