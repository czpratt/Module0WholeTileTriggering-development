'''
    Addressing the Whole Tile Triggering problem occuring in the
    Module 0 detector at LBNL

    o--- Contributers ---o
     Christian Pratt: czpratt@ucdavis.edu
     Nicholas Carrara: ncarrara.physics@gmail.com
     Jacob Steenis: jhsteenis@ucdavis.edu
    o--------------------o
'''

import h5py as h
import numpy as np
import matplotlib.pyplot as plt
import time
import yaml
import argparse
import matplotlib
from typing import Tuple, List
from scipy.spatial import ConvexHull
from collections import deque
from dataclasses import dataclass
from histogram_selection import Selection
from histogram_pulse_finder import PulseFinder
from histogram_configuration import Configuration


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='output event information')
    parser.add_argument('--datalog_file',
                        metavar='FILE',
                        type=str,
                        help='datalog file of the form (...)_CESTevd.h5')

    parser.add_argument('--geometry_file',
                        metavar='FILE',
                        type=str,
                        help='yaml file specifying the geometry')
    
    parser.add_argument('--nhits_cut',
                        metavar='NHITS CUT',
                        type=int,
                        default=None,
                        help='cut for number of hits on a tile') 

    args  = parser.parse_args()
   
    if not args.nhits_cut:
        print('\n**************************************')
        print('*** ERROR: SPECIFY nhits_cut VALUE ***')
        print('***   bad error will be thrown.    ***')
        print('**************************************\n')
    else:
        pass

    ''' Obtain selected datalog file information '''
    selection = Selection(args.datalog_file, 
                          args.geometry_file, 
                          args.nhits_cut)
    
    if args.nhits_cut:
        print(selection)
     
    ''' Obtain pulses from nhit cut events '''
    n                = 16
    time_step        = 1
    q_thresh         = float(1000)
    max_q_window_len = 5

    pulse_finder = PulseFinder(n,
                               time_step,
                               q_thresh, 
                               max_q_window_len)

    pulse_finder.find_pulses(selection)
