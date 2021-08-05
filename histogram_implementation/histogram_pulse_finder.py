'''
    Development script for histogram-based pulse finder
    *** WORK IN PROGRESS ***
'''

from selection import Selection
from collections import deque
from collections import Counter
from dataclasses import dataclass
from scipy.spatial import ConvexHull
import time
import numpy as np
import argparse
import h5py as h


@dataclass
class Pulse:
    ''' Individual pulse creation '''
    event_id: int
    tile_id: int
    hit_at_start_time: int
    hit_at_end_time: int
    pulse_start_time: int
    pulse_end_time: int
    delta_t: int
    total_q: float
    peak_q: float
    peak_q_hit_id: int
    peak_q_hit_time: int
    peak_q_hit_x: float
    peak_q_hit_y: float
    pulse_area: float


class ChargeWindow:
    ''' Individual charge window that can be created '''
    def __init__(self,
                 max_q_window_len: int,
                 q_thresh: float):
                 
        self.window           = deque()
        self.max_q_window_len = max_q_window_len
        self.q_thresh         = q_thresh
        self.pulse_indicator  = None 
    
    
    def __repr__(self):
        return ('{}'.format(self.window))


    def check_length(self):
        ''' Verifies length of window '''
        if len(self.window) < self.max_q_window_len:
            pass
        else:
            self.window.popleft()

    def set_pulse_indicator(self,
                            decision):
        ''' Sets the pulse indicator '''
        self.pulse_indicator = decision


    ### function for handling charge stuff ###





        
def assemble_charge_window_dict(max_q_window_len,
                                q_thresh,
                                n):
    ''' Creates dictionary for all charge windows '''
    window_dict = {}
    for i in range(1, n + 1, 1):
        q_window = ChargeWindow(max_q_window_len,
                                q_thresh)

        window_dict[i] = q_window

    return window_dict


def main():
    parser = argparse.ArgumentParser(description='output event information')
    parser.add_argument('--datalog_file',
                        metavar='FILE',
                        type=str,
                        help='datalog file of the form (...)_CESTevd.h5')

    parser.add_argument('--geometry_file',
                        metavar='FILE',
                        type=str,
                        help='yaml file specifying the geometry')

    args  = parser.parse_args()


    try:
        data_file = h.File(args.datalog_file, 'r')
    except FileNotFoundError:
        print('Data file ({}) could not be imported'.format(args.data_file))

    print('data file: {}'.format(data_file))
    events = data_file['events']
    hits = data_file['hits']
    
    event_id = 57130
    event = events[event_id]
    event_hits = hits[event['hit_ref']]

    # we'll still need 16 stacks for each tile!
    n = 16
    max_q_window_len = 5
    q_thresh = 1000

    window_dict = assemble_charge_window_dict(max_q_window_len,
                                              q_thresh,
                                              n)
    

main()
