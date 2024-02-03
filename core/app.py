import logging
from contextlib import suppress
from pathlib import Path
from tkinter import filedialog

import customtkinter as tk
import cv2
from PIL import Image

from core.ui import MyFrame
from utils import OPTION, VIDEOSIZE

output_path = Path("output")
output_path.mkdir(exist_ok=True)


class VideoFrameError(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)


class APP(tk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame = MyFrame(master=self, width=1080, height=720)
        self.frame.grid(row=1, column=1)
        self.video: cv2.VideoCapture  # 视频
        self.cut_point = 0  # 当前切割点
        self.image: tk.CTkImage

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
        self.move_cursor(self.play_step_frame)
        self.update_frame_pos()
        self.frame.video_info.update_info()
        self.play_video()

    def step_backward(self):
        """
        向前移动一步 cursor，并播放视频片段
        """
        self.move_cursor(-self.play_step_frame)
        self.update_frame_pos()
        self.frame.video_info.update_info()
        self.play_video()

    def open_video(self):
        """
        打开视频文件
        """
        file_path = filedialog.askopenfilename()
        logging.info("Opening video file: " + file_path)
        self.frame.video_path_label.configure(text=file_path)
        self.video = cv2.VideoCapture(file_path)
        assert self.video.isOpened(), "Video is not opened"
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEOSIZE[0])
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEOSIZE[1])
        self.cut_point = 0
        logging.debug(
            f"视频帧率：{self.fps}，视频总帧数：{self.frame_count}，视频总时间：{self.get_total_time}"
        )
        self.frame.video_info.update_info()
        self.frame.update_button_status(self)
        self.play_video()

    def play_video(self):
        """
        播放一个视频片段
        """
        self.update_frame_pos()
        while self.video_frame <= self.cut_point + self.play_step_frame:
            with suppress(VideoFrameError):
                self.show_next_frame()

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
        self.image = tk.CTkImage(Image.fromarray(frame), size=VIDEOSIZE)
        self.frame.video_frames.configure(image=self.image)
        self.frame.video_frames.update()

    def save_segment(self):
        """
        保存视频片段
        """
        option_num: int = self.frame.label_option.num.get()
        emotion = OPTION[option_num]
        output_path_sub = output_path / emotion
        output_path_sub.mkdir(exist_ok=True)
        video_index: int = len(list(output_path_sub.glob("*"))) + 1
        self.write_segment(
            output_path_sub / ".".join((emotion, str(video_index), "avi"))
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
            self.fps,
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
