import logging
from tkinter import filedialog

from core.PlayVideo import play_video, read_frame


def open_video(app):
    file_path = filedialog.askopenfilename()
    logging.info("Opening video file: " + file_path)
    app.frame.video_path_label.configure(text=file_path)
    app.open_video(file_path)
    read_frame(app.video, app.frame.video_frames)


def next_segment(app):
    app.step_forward()
    play_video(app)


def prev_segment(app):
    app.step_backward()
    play_video(app)
