"""Custom Frame-based modifiers 

    Helpers:
        build_from_list : Builds an mp4 from a list of frames        

    Methods:
        horiz_build : Equal Horizontal Splicing
"""
import numpy as np
import cv2
from utils.helpers import build_from_list

def horiz_build(schedule, ref, fps):
    """Equally Spaced Horizontal Split
    """
    imgs = [] # init list of frames (final video with run at `self.hcf_fps` fps)

    # Get schedule keys and sort frame-order (keys == frame number)
    keys = [int(k) for k in list(schedule.keys())] # str-key -> int-key and sort from low->high
    keys.sort()
    # Loop through sorted keys
    for key in keys:
        parts = schedule[str(key)] # load all

        p_list = []
        for i in range(1000):
            if str(i) in list(parts.keys()):
                p_list.append(parts[str(i)])
            else:
                break

        img_ = np.concatenate(p_list, axis=1) # finalise new frame
        
        h,w = img_.shape[0], img_.shape[1] # get height and width of frame

        for i in range(ref['total']):
            if i != ref['total']-1:
                h_ = (h/ref['total'])*(i+1)
                im  = cv2.line(img_, (0, int(h_)), (w, int(h_)), (255, 0, 0), thickness=2) # Add line splitting views

        imgs.append(im)

    # Build Video
    build_from_list(imgs, fps, h, w)