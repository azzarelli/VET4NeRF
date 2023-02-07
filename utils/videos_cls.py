import cv2
import numpy as np

from os import listdir
from os.path import isfile, join

from utils.helpers import get_duration, get_frames_fps, build_from_list
from utils.custom_modifiers import vert_split
from utils.custom_builders import default_build

def get_video_paths(path):
    return [join(path, f) for f in listdir(path) if (isfile(join(path, f))) and ('mp4' in f)]     

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

        print('Filling Schedule...')
        """Fill the image scheduler with frames
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

                # Image Modification Function : returns image of slice in the format you want to build it in
                im = func(frame=imgs[k_].copy(), id=k_, ref=self.slice_ref)

                self.p_schedule[key][str(sec)] = im # Save the images to parts-scheduler
        
    def build(self, func=default_build, fps:int=0):
        """Build video
        """
        if fps == 0: fps =self.hcf_fps

        print('Building video...')
    
        # Run custom build function from modified parts schedule
        res = func(self.p_schedule, self.slice_ref, fps) # CREATE YOUR OWN (particularly if the videos have different fps and duration and if modifications are non-linear)

        build_from_list(*res) # build the file