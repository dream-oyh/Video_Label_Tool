import tkinter as tk

import cv2
from PIL import Image, ImageTk


def play_video(app, play_time=3):
    """
    video: 视频
    video_frames: 视频播放 Label 控件
    play_time：每个间隔视频播放时间/s
    """

    video: cv2.VideoCapture = app.video
    video_frames: tk.Label = app.frame.video_frames
    video.set(cv2.CAP_PROP_POS_FRAMES, round(app.current_frame))
    play_count = play_time * app.fps  # 3 秒内的视频总帧数
    while (
        video.isOpened()
        and video.get(cv2.CAP_PROP_POS_FRAMES) <= app.current_frame + play_count
    ):
        if not read_frame(video, video_frames):
            return


def read_frame(video: cv2.VideoCapture, video_frames: tk.Label) -> bool:
    ret, readyframe = video.read()
    if not ret or readyframe is None:
        return False
    frame = cv2.cvtColor(readyframe, cv2.COLOR_BGR2RGBA)  # 转至 RGB 色彩空间
    image = ImageTk.PhotoImage(Image.fromarray(frame).resize((540, 360)))
    video_frames.configure(image=image)
    video_frames.image = image
    video_frames.update()
    return True
