'''
    Addressing the Whole Tile Triggering problem occuring in the
    Module 0 detector at LBNL

    Version 1.0.4

    o---------------- Contributers  ----------------o
    | Christian Pratt:  czpratt@ucdavis.edu         |
    | Nicholas Carrara: ncarrara.physics@gmail.com  |
    | Jacob Steenis:    jhsteenis@ucdavis.edu       |
    o-----------------------------------------------o
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

from tile_plot import *
from selection import Selection
from pulse_finder import PulseFinder
from configuration import Configuration
from wtt_display import WholeTileTriggerDisplay

matplotlib.rcParams['text.usetex'] = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='output event information')
    parser.add_argument('--datalog_file',
                        metavar='DATALOG FILE',
                        type=str,
                        help='datalog file of the form (...)_CESTevd.h5')

    parser.add_argument('--geometry_file',
                        metavar='GEOMETRY FILE',
                        type=str,
                        help='yaml file specifying the geometry')
    
    parser.add_argument('--nhits_cut',
                        metavar='NHITS CUT VALUE',
                        type=int,
                        default=None,
                        help='cut for number of hits on a tile') 

    parser.add_argument('--display_pulses',
                        action='store_true',
                        default=False)
    
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
    delta_time_slice = 5
    q_thresh         = float(50000)
    max_q_window_len = delta_time_slice


    pulse_finder = PulseFinder(n,
                               time_step,
                               q_thresh, 
                               max_q_window_len,
                               delta_time_slice)

    event_pulses = pulse_finder.find_pulses(selection)

    print('event_pulses: {}'.format(event_pulses))
    
    ''' Display pulse (WTT) information '''
    if args.display_pulses:
        pulse_data_file = ['', args.datalog_file, '']
        with open('wtt_information.txt', 'a') as f:
            f.writelines('\n'.join(pulse_data_file))
        
        with open('datalog_files_processed.txt', 'a') as f:
            f.writelines('\n'.join(pulse_data_file))
        
        wtt_display = WholeTileTriggerDisplay(event_pulses,
                                              q_thresh,
                                              delta_time_slice)

        wtt_display.display_wtt_events(selection)
