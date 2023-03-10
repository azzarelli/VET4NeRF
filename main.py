# import cv2
# import datetime
# from os import listdir
# from os.path import isfile, join
# import numpy as np
# from utils.helpers import get_duration, get_frames_fps

from utils.videos_cls import Editor

import utils.custom_modifiers as mod
import utils.custom_builders as bob
# local video directory (place all videos you want to interlace into this folder)
vid_path = 'movies/'

if __name__ == '__main__':

    ed = Editor(path=vid_path)
    ed.generate_schedule()
    ed.modify(func=mod.horiz_split)
    ed.build()

    # ed.modify(func=mod.horiz_split)
    # ed.build(func=bob.horiz_build)

