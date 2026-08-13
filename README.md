# Gold CREST Trailer Design Project

This repository contains the Python source code which makes up the two models I used in my Gold CREST project, to investigate:

1. low-speed reversing stability and manoeuvrability.
2. high-speed dynamic stability and trailer sway.

## Repository structure

- `KinematicModel/` – kinematic model for primary investigation.
- `DynamicSwayModel/` – dynamic model for supporting investigation.

## Requirements
- Python 3
- NumPy
- Matplotlib

## Folder Contents
Each folder contains the calculation function, input configurations and graph production program used for their respective investigations. The kinematic model also contains an animation. 

## Running and Using the Files
Files should be run within their model folders so that the appropriate local imports can be found.

Using the graph production files requires the most thoughtful use and input selection. Labels for legends, titles and variables to be plotted all need to be chosen and written. As these are frequently changed to produce different graphs when testing the project I cannot be sure what they will look like at this point in time. The original functions will all still function properly but selecting which to use and what inputs they require may require more thought. I have tried to provide comments beneath detailing what the suitable inputs are. 
