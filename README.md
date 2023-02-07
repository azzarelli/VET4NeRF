# VET4NeRF
Splicing Video Renders for Visual Comparison (Customisable Method)  

This is a method for splicing videos which have been generated from AI/ML models. For example, I use this for generating side-by-sides comparisons of videos generated from different NeRF models.

## Requirements

Run `pip install opencv-ptyhon` (un-tested with `conda` envs) 

## Repo Status

- [x] Videos with same camera and path parameters (untested with variation durations/fps)
- [x] Custom functions for splicing and building 
- [x] Default vertical split and linear concatenation of N videos
- [ ] Option for horizontal split
- [ ] Option for transitioning vertical/horizontal split

## Instructions for Execution

1. Declare path to folder all containing videos in `main.py`
2. Run `main.py`

Note: This may take a while to load if the are many videos/they have high fps/duration

## Instructions for Customisation
### Prelude
The methods is run through a class called `Editor` which accomplishes three tasks: 

(1) Build a frame-schedule; this finds the highest common factor of fps for all videos and saves where each frame from each video falls along the global timeline

(2) Pixel-wise modification of frame-images; this sifts through the frame-scheduler and modifies frames relative to:

- - [x] Their 'slice-id' (images from the same video have the same slice id)
 - - [ ] Frame number (for transition effects)
 - - [x] Customisable modification

(3) Builds video from schedule of modified images;

- - [x] Default linear concatenation along the x-axis
 - - [x] Custom function
 - - [ ] Handles incomplete groups of frames in schedule (e.g. when the total number of image slices at frame, f, is not equal to total number of videos)

### Custom Frame Modificatier

The class-method `Editor.modify` can take the argument `func=myCustomFunction`. The following block demonstrates custom function definition:

```
def myCustomFunction(frame:np.ndarray, id:int, ref:dict):
    ...
    return modified_image
    
editor = Editor(...)

...

ed.modify(func=myCustomFunction)
```

where `frame` is the (N, M, 3) numpy array for NxM BGR image, `id` is the video id of the frame for [0, 1, ..., P] videos, ref is a dictionary referencing `id` to path (`id[total]` can be called to fetch the total number of videos)


### Custom Video Builder

