from pathlib import Path

import customtkinter as tk
import cv2
from PIL import Image

from utils import OPTION

output_path = Path("output")
output_path.mkdir(exist_ok=True)


def play_video(app):
    video: cv2.VideoCapture = app.video
    play_count: float = app.play_step * app.fps
    app.update_frame_pos()
    while (
        video.isOpened()
        and video.get(cv2.CAP_PROP_POS_FRAMES) <= app.current_frame + play_count
    ):
        if not show_next_frame(video, app.frame.video_frames):
            return


def show_next_frame(video: cv2.VideoCapture, video_frames: tk.CTkLabel) -> bool:
    """
    显示一帧，返回一个 bool 值代表是否成功
    """
    ret, readyframe = video.read()
    if not ret or readyframe is None:
        return False
    frame = cv2.cvtColor(readyframe, cv2.COLOR_BGR2RGBA)  # 转至 RGB 色彩空间
    image = tk.CTkImage(Image.fromarray(frame), size=(720, 480))
    video_frames.configure(image=image)
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
    video = app.video
    play_count = app.play_step * app.fps
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    app.update_frame_pos()
    out = cv2.VideoWriter(
        str(path.absolute()),
        fourcc,
        app.fps,
        (
            int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        ),
    )

    while (
        video.isOpened()
        and video.get(cv2.CAP_PROP_POS_FRAMES) <= app.current_frame + play_count
    ):
        ret, frame = video.read()
        if not ret or frame is None:
            break
        else:
            out.write(frame)
