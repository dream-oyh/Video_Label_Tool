import tkinter as tk
import cv2
from core.PlayVideo import PlayVideo


class LoadButton(tk.Button):
    def __init__(self, **kwargs):
        kwargs = {"command": self.load_video, **kwargs}
        super().__init__(**kwargs)

    def load_video(self):
        # assert self.master.video_path_label.text, "Please open the files first"
        self.video = self.master.file_open_button.video
        self.video_frames = self.master.video_frames
        self.FPS = self.master.file_open_button.FPS
        self.master.file_open_button.time += 3 * self.master.file_open_button.FPS
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.master.file_open_button.time)
        PlayVideo(self.video, self.video_frames)
