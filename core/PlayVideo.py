import tkinter as tk

import cv2
from PIL import Image, ImageTk


def play_video(app, play_time=3, wait_time=1):
    """
    video: 视频
    video_frames: 视频播放 Label 控件
    play_time：每个间隔视频播放时间/s
    wait_time: 每帧停留时间，控制播放帧速率
    """

    video: cv2.VideoCapture = app.video
    video_frames: tk.Label = app.frame.video_frames
    video.set(cv2.CAP_PROP_POS_FRAMES, round(app.current_frame))
    i = 0
    play_count = play_time * app.fps  # 3 秒内的视频总帧数
    while video.isOpened() and i < play_count:
        ret = read_frame(video, video_frames)
        i = i + 1
        if not ret:
            break


def read_frame(video: cv2.VideoCapture, video_frames: tk.Label) -> bool:
    ret, readyframe = video.read()
    if readyframe is None:
        return False
    if ret:
        frame = cv2.cvtColor(readyframe, cv2.COLOR_BGR2RGBA)  # 转至 RGB 色彩空间
        image = ImageTk.PhotoImage(Image.fromarray(frame).resize((540, 360)))
        video_frames.configure(image=image)
        video_frames.image = image
        video_frames.update()
    return ret
