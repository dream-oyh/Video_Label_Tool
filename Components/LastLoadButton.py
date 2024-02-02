import tkinter as tk
import cv2
from .LoadButton import LoadButton
from core.PlayVideo import PlayVideo


class LastLoadButton(tk.Button):
    def __init__(self, **kwargs):
        kwargs = {"command": self.OpenFun, **kwargs}
        super(LastLoadButton, self).__init__(**kwargs)

    def OpenFun(self):
        self.video = self.master.file_open_button.video
        self.video_frames = self.master.video_frames
        self.FPS = self.master.file_open_button.FPS
        self.master.file_open_button.time -= 3 * self.master.file_open_button.FPS
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.master.file_open_button.time)
        PlayVideo(self.video, self.video_frames)
