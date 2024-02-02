import customtkinter as tk


class SubInfo(tk.CTkFrame):
    def __init__(self, text, val, master, **kwargs):
        super().__init__(master, **kwargs)
        self.text_label = tk.CTkLabel(master=self, text=text)
        self.text_label.grid(row=1, column=1)
        self.val = tk.CTkLabel(master=self, text=str(val))
        self.val.grid(row=1, column=2)


class InfoFrame(tk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.fps_label = SubInfo(master=self, text="视频帧率：", val=0)
        self.fps_label.grid(row=1, column=1, sticky="w")

        self.totaltime_label = SubInfo(master=self, text="视频总时长：", val=0)
        self.totaltime_label.grid(row=2, column=1, sticky="w")

        self.frame_count_label = SubInfo(master=self, text="视频总帧数：", val=0)
        self.frame_count_label.grid(row=3, column=1, sticky="w")

        self.cut_point_label = SubInfo(master=self, text="当前段起点帧：", val=0)
        self.cut_point_label.grid(row=4, column=1, sticky="w")

        self.current_time_label = SubInfo(
            master=self,
            text="当前段起点时间：",
            val=0,
        )
        self.current_time_label.grid(row=5, column=1, sticky="w")

    def update_info(self):
        app = self.master.master
        self.totaltime_label.val.configure(text=str(app.get_total_time))
        self.fps_label.val.configure(text=str(app.fps))
        self.frame_count_label.val.configure(text=str(app.frame_count))
        self.cut_point_label.val.configure(text=str(app.cut_point))
        self.current_time_label.val.configure(text=str(app.current_time))
