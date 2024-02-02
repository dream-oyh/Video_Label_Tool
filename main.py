import logging
import tkinter as tk

import cv2

from core.ui import MyFrame

logging.basicConfig(level=logging.DEBUG)


class APP(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame = MyFrame(master=self, width=1080, height=720)
        self.frame.grid(row=1, column=1)
        self.video: cv2.VideoCapture  # 视频
        self.step_time: float = 3  # 步长（时间）
        self.current_frame = 0  # 当前帧

    @property
    def fps(self) -> float:
        """
        视频帧率
        """
        return self.video.get(cv2.CAP_PROP_FPS)

    @property
    def frame_count(self) -> float:
        """
        视频总帧数
        """
        return self.video.get(cv2.CAP_PROP_FRAME_COUNT)

    @property
    def get_total_time(self) -> float:
        """
        视频总时间
        """
        return self.frame_count / self.fps

    def open_video(self, path: str):
        self.video = cv2.VideoCapture(path)
        logging.debug(
            f"视频帧率：{self.fps}，视频总帧数：{self.frame_count}，视频总时间：{self.get_total_time}"
        )

    def step_forward(self):
        temp = self.step_time * self.fps
        if self.current_frame + temp <= self.frame_count:
            self.current_frame += temp
        logging.info(
            f"当前帧：{self.current_frame}，当前时间：{self.current_frame / self.fps}"
        )
        logging.debug(f"temp: {temp}")

    def step_backward(self):
        temp = self.step_time * self.fps
        if self.current_frame - temp >= 0:
            self.current_frame -= temp
        logging.info(
            f"当前帧：{self.current_frame}，当前时间：{self.current_frame / self.fps}"
        )


app = APP()
app.title("Video Label Tool")
app.geometry("1080x720")
try:
    app.mainloop()
finally:
    app.video.release()
    cv2.destroyAllWindows()
    logging.info("程序结束")
