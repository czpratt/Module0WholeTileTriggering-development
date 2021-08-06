'''
    Development script for histogram-based pulse finder
    *** WORK IN PROGRESS ***
'''

from histogram_selection import Selection
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



class PulseFinder:
    ''' Class for finding pulses within a TPC waveform '''
    def __init__(self,
                  max_q_window_length: int,
                  q_threshold: float,
                  time_step: int
                  n: int):

        self.time_step           = time_step
        self.q_thresh            = q_thresh
        self.max_q_window_length = max_q_window_len
        
        self.event      = None
        self.hits       = None
        self.event_hits = None
        self.hit_count  = None


    def obtain_event_pulses(self,
                            selection,
                            tiles_and_hits):
        ''' Attempts to find pulses in an event '''
        # histogram implementation goes here



    def find_pulses(self,
                    selection):
        ''' Main driver of pulse scanning '''
        cut_events = selection.get_cut_events()
        start_time = time.time()

        for evid in cut_events.keys():
            print('evaluating event {}'.format(evid))
            self.event      = selection.get_event(evid)
            self.event_hits = selection.get_event_hits(self.event)
            tiles_and_hits  = cut_events[evid]
            event_pulses = self.obtain_event_pulses(selection,
                                                    tiles_and_hits)
        
        end_time = time.time()
        print('scan for pulses completed in {} seconds'.format(end_time - start_time))
        
