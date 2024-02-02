import tkinter as tk
from tkinter import filedialog
from core.PlayVideo import read_frame
import cv2


class FileOpenButton(tk.Button):
    def __init__(self, **kwargs):
        self.command = self.OpenFun
        super().__init__(command=self.command, **kwargs)

    def OpenFun(self):
        self.file_path = filedialog.askopenfilename()
        print(self.file_path)
        self.master.video_path_label.configure(text=self.file_path)
        self.video = cv2.VideoCapture(self.file_path)
        self.FPS = self.video.get(cv2.CAP_PROP_FPS)
        self.time = -3 * self.FPS
        read_frame(self.video, self.master.video_frames)
