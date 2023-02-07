# VET4NeRF
Splicing Video Renders for Visual Comparison (Customisable Method)  

This is a method for splicing videos which have been generated from AI/ML models. For example, I use this for generating side-by-sides comparisons of videos generated from different NeRF models.

## Requirements

Run `pip install opencv-ptyhon` (un-tested with `conda` envs) 


## Instructions for Execution

1. Declare path to folder all containing videos in `main.py`
2. Run `main.py`

Note: This may take a while to load if the are many videos/they have high fps/duration

## Repo Status

└&#x2611; Videos with same camera and path parameters

└&#x2611; Custom functions for splicing and building 

  └&#x2611; Default vertical split and linear concatenation of N videos
  
  └&#x2610;Option for horizontal split
  
  └&#x2610; Transitioning vertical/horizontal split
