"""Custom Fame-based modifiers 

    Methods:
        vert_split : Equal Vertical Splicing
        horiz_split : Equal Horizontal Splicing
"""
import numpy as np
def vert_split(frame=None, id=None, ref=None):
    """Example of custom vertical split function
    """
    if type(id) != type(None):
        sl = ref[id] # get slice id
        tot_sl = ref['total'] # get total slices

        h,w = frame.shape[0], frame.shape[1] # get height and width of frame

        idx_start = (float(sl)/float(tot_sl))*w # get start index and end index for vertical points
        idx_end = ((float(sl)+1.)/float(tot_sl))*w
        
        frame_ = np.zeros(frame.shape, dtype=np.uint8)
        frame_[:,int(idx_start):int(idx_end)] = frame[:,int(idx_start):int(idx_end)].copy()

        # part = frame[:,int(idx_start):int(idx_end)] # slice (crop) frame matrix

        return frame_
        
    else:
        print('incorrect inputs')
        exit()

def horiz_split(frame=None, id=None, ref=None):
    """Example of custom vertical split function
    """
    if type(id) != type(None):
        sl = ref[id] # get slice id
        tot_sl = ref['total'] # get total slices

        h,w = frame.shape[0], frame.shape[1] # get height and width of frame

        idx_start = (float(sl)/float(tot_sl))*w # get start index and end index for vertical points
        idx_end = ((float(sl)+1.)/float(tot_sl))*w
        
        frame_ = np.zeros(frame.shape, dtype=np.uint8)
        frame_[int(idx_start):int(idx_end), :] = frame[int(idx_start):int(idx_end), :].copy()

        # part = frame[:,int(idx_start):int(idx_end)] # slice (crop) frame matrix

        return frame_
        
    else:
        print('incorrect inputs')
        exit()