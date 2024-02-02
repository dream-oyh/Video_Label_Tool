from pathlib import Path

import customtkinter as tk
import cv2
from PIL import Image

from utils import OPTION

output_path = Path("output")
output_path.mkdir(exist_ok=True)


def video_info(app):
    video: cv2.VideoCapture = app.video
    play_time = app.set_play_time
    video.set(cv2.CAP_PROP_POS_FRAMES, round(app.current_frame))
    play_count = play_time * app.fps  # 3 秒内的视频总帧数
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return video, play_count, width, height


def play_video(app):
    video, play_count, _, _ = video_info(app)
    video_frames: tk.CTkLabel = app.frame.video_frames
    while (
        video.isOpened()
        and video.get(cv2.CAP_PROP_POS_FRAMES) <= app.current_frame + play_count
    ):
        if not read_frame(video, video_frames):
            return


def read_frame(video: cv2.VideoCapture, video_frames: tk.CTkLabel) -> bool:
    ret, readyframe = video.read()
    if not ret or readyframe is None:
        return False
    frame = cv2.cvtColor(readyframe, cv2.COLOR_BGR2RGBA)  # 转至 RGB 色彩空间
    image = tk.CTkImage(Image.fromarray(frame), size=(720, 480))
    video_frames.configure(image=image)
    video_frames.image = image
    video_frames.update()
    return True


def save_video(app):
    option_num: int = app.frame.label_option.num.get()
    emotion = OPTION[option_num]
    output_path_sub = output_path / emotion
    output_path_sub.mkdir(exist_ok=True)
    video_index: int = len(list(output_path_sub.glob("*.avi"))) + 1
    write_video(app, output_path_sub / ".".join((emotion, str(video_index), "avi")))


def write_video(app, path: Path):
    video, play_count, width, height = video_info(app)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    out = cv2.VideoWriter(str(path.absolute()), fourcc, app.fps, (width, height))

    while (
        video.isOpened()
        and video.get(cv2.CAP_PROP_POS_FRAMES) <= app.current_frame + play_count
    ):
        ret, frame = video.read()
        if not ret or frame is None:
            break
        else:
            out.write(frame)
