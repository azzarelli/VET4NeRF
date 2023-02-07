"""Custom Fame-based modifiers 

    Methods:
        horiz_split : Equal Horizontal Splicing
"""
def horiz_split(frame=None, id=None, ref=None):
    """Example of custom vertical split function
    """
    if type(id) != type(None):
        sl = ref[id] # get slice id
        tot_sl = ref['total'] # get total slices

        h,w = frame.shape[0], frame.shape[1] # get height and width of frame

        idx_start = (float(sl)/float(tot_sl))*h # get start index and end index for vertical points
        idx_end = ((float(sl)+1.)/float(tot_sl))*h
        part = frame[int(idx_start):int(idx_end), :] # slice (crop) frame matrix

        return part
    
    else:
        print('incorrect inputs')
        exit()