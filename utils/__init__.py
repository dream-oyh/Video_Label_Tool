import logging
from tkinter import filedialog

from core.Video import play_video


def open_video(app):
    file_path = filedialog.askopenfilename()
    logging.info("Opening video file: " + file_path)
    app.frame.video_path_label.configure(text=file_path)
    app.open_video(file_path)

    play_video(app)
    # app.frame.view_info()


def next_segment(app):
    app.step_forward()
    play_video(app)


def prev_segment(app):
    app.step_backward()
    play_video(app)

    # match option_val:
    #     case 1:
    #         Path("./label_folder/"+option[0]).mkdir(parents=True, exist_ok=True)
    #     case 2:
    #         Path("./label_folder/"+option[1]).mkdir(parents=True, exist_ok=True)
    #     case 3:
    #         Path("./label_folder/"+option[2]).mkdir(parents=True, exist_ok=True)
    #     case 4:
