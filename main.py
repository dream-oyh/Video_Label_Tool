import logging
import threading

import cv2

from core.app import APP

logging.basicConfig(level=logging.DEBUG)


app = APP()
app.title("Video Label Tool")
width = app.frame.cget("width")
height = app.frame.cget("height")
app.geometry(str(width) + "x" + str(height))
app.bind("<Return>", lambda event: threading.Thread(target=app.save_segment).start())
app.bind("<Key-n>", lambda _: app.step_forward())
try:
    app.mainloop()
finally:
    if t := getattr(app, "video", None):
        t.release()
    cv2.destroyAllWindows()
    logging.info("程序结束")
    exit(0)
