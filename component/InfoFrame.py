import tkinter as tk


class SubInfo(tk.Frame):
    def __init__(self, text, val, **kwargs):
        super().__init__(**kwargs)
        self.text_label = tk.Label(text=text)
        self.text_label.pack(side='left', anchor='nw')
        self.val = tk.Label(text=str(val))
        self.val.pack(side='left', anchor='nw')


class InfoFrame(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.totaltime_label = SubInfo(
            text="视频总时长：", val=self.master.master.get_total_time
        )
        self.totaltime_label.pack()

        self.fps_label = SubInfo(text="视频帧率：", val=self.master.master.fps)
        self.fps_label.pack()

        self.frame_count_label = SubInfo(
            text="视频总帧数：", val=self.master.master.frame_count
        )
        self.frame_count_label.pack()

        self.current_frame_label = SubInfo(
            text="当前帧数：", val=self.master.master.current_frame
        )
        self.current_frame_label.pack()

        self.current_time_label = SubInfo(
            text="当前时间：",
            val=self.master.master.current_frame / self.master.master.fps,
        )
        self.current_time_label.pack()
