import logging

import customtkinter as tk
import cv2

from core.ui import MyFrame


class APP(tk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame = MyFrame(master=self, width=1080, height=720)
        self.frame.grid(row=1, column=1)
        self.video: cv2.VideoCapture  # 视频
        self.current_frame = 0  # 当前帧

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
    def play_step(self) -> int:
        """
        获取播放步长
        """
        return self.frame.playtime.get()

    def update_frame_pos(self):
        """
        更新当前帧位置
        """
        self.video.set(cv2.CAP_PROP_POS_FRAMES, round(self.current_frame))

    def open_video(self, path: str):
        self.video = cv2.VideoCapture(path)
        logging.debug(
            f"视频帧率：{self.fps}，视频总帧数：{self.frame_count}，视频总时间：{self.get_total_time}"
        )
        self.frame.video_info.update_info()

    def step_forward(self):
        temp = round(self.play_step * self.fps)
        if self.current_frame + temp <= self.frame_count:
            self.current_frame += temp
        self.frame.video_info.update_info()
        logging.info(
            f"当前帧：{self.current_frame}，当前时间：{self.current_frame / self.fps}"
        )
        logging.debug(f"temp: {temp}")

    def step_backward(self):
        temp = round(self.play_step * self.fps)
        if self.current_frame - temp >= 0:
            self.current_frame -= temp
        self.frame.video_info.update_info()
        logging.info(
            f"当前帧：{self.current_frame}，当前时间：{self.current_frame / self.fps}"
        )
