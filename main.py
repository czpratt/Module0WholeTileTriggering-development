'''
    Revising whole_tile_triggering
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
from configuration import Configuration

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

    parser.add_argument('--nhit_cut',
                        metavar='NHITS CUT',
                        type=int,
                        default=None,
                        help='cut for number of hits on a tile') 

    args  = parser.parse_args()
    
    ''' Obtain selected datalog file information '''
    selection = Selection(args.datalog_file, args.geometry_file, args.nhit_cut)
    
    if args.nhit_cut:
        print('all nhit cut events: {}'.format(selection.get_nhit_cut_events()))
     
    ''' Obtain pulses from events '''

