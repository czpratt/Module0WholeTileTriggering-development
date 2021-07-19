## Module 0 Whole Tile Triggering ##

Investigating the whole tile triggering problem associated with the Module 0 detector at LBNL.

This repository functions as the current codebase for investigating the whole tile triggering problem associated with the Module 0 detector at LBNL. The current physical candidates causing these occurences include but are not limited to: 

* High energy electromagnetic showers
* Sync pulses being generated at 1 Hz

To run the driver code of the investigation:

1. Clone the repository
2. Run `python3 main.py --datalog_file={datalog file} --geometry_file={tile layout file}`, where you can download a [datalog file](https://portal.nersc.gov/project/dune/data/Module0/TPC1+2/dataRuns/evdData/) (it is currently optimal to download any file > 200Mb) and a [tile layout file](https://portal.nersc.gov/project/dune/data/Module0/) (current version: `multi_tile_layout-2.1.16.yaml`)

### Current Project Roadmap ###

- [X] Implement a suite of selection algorithms to tag interesting events
    - [X] Look for events with 'nhit' > threshold for a given tile
    - [X] Find pulses within interesting events, generate useful statistics
    - [X] use scipy.spatial.ConvexHull to find the pulse area

- [] Determine the origin of the whole tile triggering problem
    - [] Is there a spatial/temporal pattern to these hits?
    - [] Does this pattern relate to the hydra network geometry?
    - [] ...

- [] Possibly implement the pulse finding algorithm as part of the event building
    - [] Are there particular widths/thresholds of interest?
    - [] Other potentially useful statistics? 
    - [] Add a 'pulses' group to the HDF5 files
    - [] ...

### Upcoming implementations ###

* Refinement of parameter values for
    1. threshold for number of hits per tile per event
    2. maximum pulse width with respect to 'sliding' charge window
* More plotting utilities (3D functionality, etc)
* Implementing more indicators for whole tile triggering identification
* More documentation

### File documentation ###

- `configuration.py`: Handles tile layout information directly from passed `.yaml` file 

- `selection.py`: Obtains information from a passed datalog file
  If a cut on the number of hits per tile per event is activated, a dictionary is returned that is formatted as:
  `{evid_1: {tile_id_1: nhits_1, tile_id_2: nhits_2, ...},
   evid_2: {tile_id_1: nhits_1, ...}
   ...
   }`

- `pulse_finder.py`: Finds pulses within events once nhit cut is made from the dictionary obtained by `selection.py`, the pulse finding algorithm attempts to find pulses based on the amount of charge deposited on a tile for a given time slot.

- `tile_plot.py`: Plotting functionality

- `main.py`: Main driver function 

### Active Contributers ###

* Nicholas Carrara, Postdoctoral Researcher, UC Davis
* Christian Pratt, Graduate Student, UC Davis
* Jacob Steenis, Graduate Student, UC Davis
