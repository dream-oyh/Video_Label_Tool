import tkinter as tk

import cv2
from PIL import Image, ImageTk


def PlayVideo(video, video_frames, play_time=3, wait_time=1):
    """
    video: 视频，cv2.VideoCapture 对象
    video_frames: 视频播放 Label 控件
    play_time：每个间隔视频播放时间
    wait_time: 每帧停留时间，控制播放帧速率
    """
    video_total_time = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(
        cv2.CAP_PROP_FPS
    )  # 帧数/帧速率得到视频总时间
    i = 1
    play_count = play_time * video.get(cv2.CAP_PROP_FPS)  # 3 秒内的视频总帧数
    video_frames.configure(text="")
    while video.isOpened() and i <= play_count:
        ret = read_frame(video, video_frames, wait_time)
        i = i + 1
        if ret == False:
            break


def read_frame(video, video_frames, wait_time=1):
    ret, readyframe = video.read()
    if ret == True:
        frame = cv2.cvtColor(readyframe, cv2.COLOR_BGR2RGBA)  # 转至 RGB 色彩空间
        new_image = Image.fromarray(frame).resize((540, 360))
        new_cover = ImageTk.PhotoImage(image=new_image)
        video_frames.configure(image=new_cover)
        video_frames.image = new_cover
        video_frames.update()  # 鬼知道我因为不知道要加这条语句，在“无法响应”里卡死了多久
        cv2.waitKey(wait_time)  # 控制帧数，但是我觉得这玩意儿好像没什么用，我也没搞清楚他怎么用的
    return ret
