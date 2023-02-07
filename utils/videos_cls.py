from utils.helpers import get_duration, get_frames_fps, build_from_list
import cv2
import numpy as np

from os import listdir
from os.path import isfile, join

def get_video_paths(path):
    return [join(path, f) for f in listdir(path) if (isfile(join(path, f))) and ('mp4' in f)]


def vert_split(frame=None, id=None, ref=None):
    """Example of custom vertical split function
    """
    if type(id) != type(None):
        sl = ref[id] # get slice id
        tot_sl = ref['total'] # get total slices

        h,w = frame.shape[0], frame.shape[1] # get height and width of frame

        idx_start = (float(sl)/float(tot_sl))*w # get start index and end index for vertical points
        idx_end = ((float(sl)+1.)/float(tot_sl))*w
        part = frame[:,int(idx_start):int(idx_end)] # slice (crop) frame matrix

        return part
        
    else:
        print('incorrect inputs')
        exit()
     

class Editor:
    def load_data(self, min_seconds:int=100000):
        """Load video object and define loading data"""

        fpss = []
        for idx, path_ in enumerate(self.path2vid):
            self.slice_ref[path_] = idx # set the slice id for each video

            obj = cv2.VideoCapture(path_) # load the video object

            d = get_duration(obj)
            frames, fps = get_frames_fps(obj)

            if d < min_seconds:
                min_seconds = d
            
            self.objects[path_] = {'obj': obj, 'duration': d, 'fps':fps, 'frames':frames}
            fpss.append(int(fps))
            
        self.slice_ref['total'] = idx+1 # set the slice length

        self.hcf_fps = np.gcd.reduce(fpss) # determined the highest common factor fps of all video fps'
        return min_seconds

    def __init__(self, path:str='', min_seconds:int=100000):
        self.search_path = path
        self.path2vid = get_video_paths(path)

        self.slice_ref = {}
        self.objects = {}
        self.hcf_fps = 0 # init highest common factor fps of videos

        min_seconds = self.load_data(min_seconds=min_seconds) # load data and fetch smallest video in files

        # Get all potential time-steps where any frame may potentially exist
        self.t_common = {f'{i}': i/self.hcf_fps for i in range(0, int(min_seconds*self.hcf_fps), 1)}

        # Create a scheduler for global frames, 
        self.t_schedule = {f'{i}':[] for i, t_ in enumerate(self.t_common)} # schedule pointing to video objs
        self.f_schedule = {} # schedule pointing to images
        self.p_schedule = {} # schedule pointing to modified frame parts

    def generate_schedule(self):
        """Generate frame-based schedule for pairing images
        """
        print('Generating Schedule...')
        self.determine_frame_schedule()
        self.fill_schedule_images()


    def determine_frame_schedule(self):
        """Determne the schedule for when each video frame (from each video) lands along the same timeline
        """
        # Note which frames from which videos apear at time t in scheduler
        for obj in self.objects:
            path = obj # fetch the path
            obj = self.objects[path] # fetch video object (dict)

            # Fetch relevant video properties
            s = obj['duration'] 
            frames = int(obj['frames'])
            fps = obj['fps']
            
            # Determine the local schedule for each video
            t_o = {f'{i}': i/fps for i in range(0, int(s*fps), 1)}

            # For each point in global schedule -> determine where local schedule intersects
            for t_ in self.t_common:
                t = self.t_common[t_]
                if t in t_o.values():
                    f = list(t_o.keys())[list(t_o.values()).index(t)]
                    self.t_schedule[t_].append({path:int(f)})

        self.f_schedule = {l:{} for l in list(self.t_schedule.keys())} # init frame schedule

    def fill_schedule_images(self):
        """Fill the image scheduler
        """
        for t_ in self.t_schedule:
            paths = self.t_schedule[t_]
            for p_ in paths:
                t_frame = list(p_.values())[0] # fetch target frame
                
                pth = list(p_.keys())[0] # fetch object path (id)
                obj = self.objects[pth]['obj']
                obj.set(1, t_frame)
                _, frame = obj.read()

                self.f_schedule[f'{t_}'][pth] = frame
    
    def modify(self, func=vert_split):
        """Load in custom function for cropping/modifying frames

            Functions are given each image-frame, its id and the slice ref and return cropped frame
        """
        print('Applying frame-wise modifications...')
        
        tot_slices = self.slice_ref['total']
        for key in list(self.f_schedule.keys()):
            self.p_schedule[key] = {}
            imgs = self.f_schedule[key]
            k = list(imgs.keys())
            n_imgs = len(k)

            for k_ in k:
                sec = self.slice_ref[k_]

                im = func(frame=imgs[k_].copy(), id=k_, ref=self.slice_ref)

                self.p_schedule[key][str(sec)] = im
        
    def build(self, func:str=None, fps:int=0):
        if fps == 0: fps =self.hcf_fps
        """Build video
        """
        print('Building video...')
        # Run custom build function from modified parts schedule
        if func != None:
            func(self.p_schedule) # CREATE YOUR OWN (particularly if the videos have different fps and duration and if modifications are non-linear)

        # Otherwise build with simple concatenation (default x axis)
        else:
            imss = [] # init list of frames (final video with run at `self.hcf_fps` fps)

            # Get schedule keys and sort frame-order (keys == frame number)
            keys = [int(k) for k in list(self.p_schedule.keys())] # str-key -> int-key and sort from low->high
            keys.sort()
            # Loop through sorted keys
            for key in keys:
                parts = self.p_schedule[str(key)] # load all

                '''ATTENTION - 
                        The order (/method) of image concatenation is important!
                    
                    We have implemented a linear-concatenation along the x axis of the image,
                    (e.g.) At each timepoint t in our parts schedule:
                            GroupOfImgParts(time=t) = (ImagePart(slice_id=0), ImagePart(slice_id=1), ..., ImagePart(slice_id=N))
                    we concatenate left-to-right in order of slice, which means the final image will place slice_id=0 on the left-
                    most side of the video frame
                
                    This default because of the default (example) `vert-split` function
                    
                    TODO - Create base set of concatenation methods
                '''

                p_list = []
                for i in range(1000):
                    if str(i) in list(parts.keys()):
                        p_list.append(parts[str(i)])
                    else:
                        break

                img_ = np.concatenate(p_list, axis=1) # finalise new frame
                
                h,w = img_.shape[0], img_.shape[1] # get height and width of frame

                for i in range(self.slice_ref['total']):
                    if i != self.slice_ref['total']-1:
                        w_ = (w/self.slice_ref['total'])*(i+1)
                        im  = cv2.line(img_, (int(w_), 0), (int(w_), h), (255, 0, 0), thickness=2) # Add line splitting views

                imss.append(im)

            build_from_list(imss, fps, h, w)
