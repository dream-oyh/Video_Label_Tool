import tkinter as tk
import cv2
from core.PlayVideo import PlayVideo


class ReLoadButton(tk.Button):
    def __init__(self, **kwargs):
        kwargs = {"command": self.reload, **kwargs}
        super().__init__(**kwargs)

    def reload(self):
        file_open_button = self.master.file_open_button
        video = file_open_button.video
        video.set(cv2.CAP_PROP_POS_FRAMES, file_open_button.time)
        video_frames = self.master.video_frames
        PlayVideo(video, video_frames)
