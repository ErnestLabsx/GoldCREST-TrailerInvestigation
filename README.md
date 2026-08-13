# Gold CREST Trailer Design Project

This repo contains the files which make up the two models I used in my gold CREST project.

1. low-speed reversing stability and manoeuvrability
2. high-speed dynamic stability and trailer sway

## Repository structure

- `primary-investigation/` – kinematic model for primary investigation
- `supporting-investigation/` – dynamic model for supporting investigation

## Requirements
- Python 3
- NumPy
- Matplotlib

## Running the models
Both investigations contain  files that holds the calculation function and sets of inputs. These should not be run or changed, unless the the user desires a set of input parametres that cannot be aquired with waht already exists in the input options file.

For the reversing investigation there is also an animation function which can be run.

Both investigatinons have graph plotting functions which allow the independent variable to be changed through a range and the results plotted in a series of graphs. The graphs and functions within each are slightly different and the code should be looked thorugh before running so that the correct graphs are plotted for the user.
