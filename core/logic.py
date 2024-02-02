# 按钮逻辑
import logging
from tkinter import filedialog

from .Video import play_video


def open_video(app):
    file_path = filedialog.askopenfilename()
    logging.info("Opening video file: " + file_path)
    app.frame.video_path_label.configure(text=file_path)
    app.open_video(file_path)
    app.frame.update_button_status(app)
    play_video(app)


def next_segment(app):
    app.step_forward()
    play_video(app)


def prev_segment(app):
    app.step_backward()
    play_video(app)
