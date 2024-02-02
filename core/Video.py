import tkinter as tk
from pathlib import Path

import cv2
from PIL import Image, ImageTk


def video_init(app):
    video: cv2.VideoCapture = app.video
    play_time = app.set_play_time
    video.set(cv2.CAP_PROP_POS_FRAMES, round(app.current_frame))
    play_count = play_time * app.fps  # 3 秒内的视频总帧数
    return video, play_count


def play_video(app):
    video, play_count = video_init(app)
    video_frames: tk.Label = app.frame.video_frames
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


def save_video(app):
    option_num = app.frame.label_option.num.get()
    match option_num:
        case 0:
            write_video(
                app,
                "label_folder/Anger/"
                + "Anger"
                + str(len(list(Path("label_folder/Anger/").glob("*.avi"))) + 1)
                + ".avi",
            )
        case 1:
            write_video(
                app,
                "label_folder/Happy/"
                + "Happy"
                + str(len(list(Path("label_folder/Happy/").glob("*.avi"))) + 1)
                + ".avi",
            )
        case 2:
            write_video(
                app,
                "label_folder/Sad/"
                + "Sad"
                + str(len(list(Path("label_folder/Sad/").glob("*.avi"))) + 1)
                + ".avi",
            )
        case 3:
            write_video(
                app,
                "label_folder/Anxious/"
                + "Anxious"
                + str(len(list(Path("label_folder/Anxious/").glob("*.avi"))) + 1)
                + ".avi",
            )


def write_video(app, path: str):
    video, play_count = video_init(app)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(path, fourcc, 20.0, (width, height))

    while (
        video.isOpened()
        and video.get(cv2.CAP_PROP_POS_FRAMES) <= app.current_frame + play_count
    ):
        ret, frame = video.read()
        if not ret or frame is None:
            break
        else:
            out.write(frame)

def view_video_info(app):
    video = app.video
    