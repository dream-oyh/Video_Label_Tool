import logging

import cv2

from core.app import APP

logging.basicConfig(level=logging.DEBUG)


app = APP()
app.title("Video Label Tool")
width = app.frame.cget('width')
height = app.frame.cget('height')
app.geometry(str(width) + "x" + str(height))
try:
    app.mainloop()
finally:
    if t := getattr(app, "video", None):
        t.release()
    cv2.destroyAllWindows()
    logging.info("程序结束")
    exit(0)
