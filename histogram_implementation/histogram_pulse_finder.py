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


class Instile:
    ''' INformation Storage about a TILE 
        - self explanatory; stores information about a tile
          throughout an event, including its charge window, 
          and potential lists to be used for histograms         '''
    def __init__(self,
                 max_q_window_len: int,
                 q_thresh: float):
                 
        self.max_q_window_len = max_q_window_len
        self.q_thresh         = q_thresh
        
        self.window      = None
        self.charges     = None
        self.time_stamps = None
        self.startup()
    
    
    def startup(self):
        ''' Initialization '''
        self.window      = deque()
        self.charges     = []
        self.time_stamps = []

    def __repr__(self):
        ''' String representation function '''
        return ('window: {}, charges = {}\n'.format(self.window,
                                                    self.charges))


    def check_window_length(self):
        ''' Verifies length of window '''
        if len(self.window) < self.max_q_window_len:
            pass
        else:
            self.window.popleft()


    def set_pulse_indicator(self,
                            decision):
        ''' Sets the pulse indicator '''
        self.pulse_indicator = decision



class PulseFinder:
    ''' Class for finding pulses within a TPC waveform '''
    def __init__(self,
                 n,
                 time_step: int,
                 q_thresh: float,
                 max_q_window_len: int):

        self.nwindows          = n                    # number of windows/tiles
        self.time_step         = time_step            # timestep
        self.q_thresh          = q_thresh             # charge threshold
        self.max_q_window_len  = max_q_window_len     # maximum length of charge window

        self.event      = None
        self.hits       = None
        self.event_hits = None
        self.hit_count  = None

        self.event_start_time = None
        self.event_end_time   = None

        self.instile_dict = None
   
        self.NO_Q   = 0

    def assemble_instile_dict(self):
        ''' Creates dictionary of charge windows for each tile '''
        instile_dict = {}
        for tile in range(1, self.nwindows + 1, 1):
            instile = Instile(self.max_q_window_len,
                              self.q_thresh)
    
            instile_dict[tile] = instile
    
        return instile_dict


    def reinitialize(self):
        ''' Reinitialization of certain variables '''
        self.instile_dict     = None
        self.event_start_time = None
        self.event_end_time   = None
        self.time_stamps      = None
        self.hit_count        = 0

    
    def append_charge_and_time(self,
                               tile_id,
                               charge):
        ''' 
            Appends charge and time to appropriate lists 
            instile == tile_id
            self.instile_dict[instile] == tile information
            --- a couple scenarios:
            - if hit occurred at timestamp, append corresponding charge and timestamp
            - if no hit occurred at timestamp, append 0 charge and the timestamp 
            NOTE: multiple hits can be logged at the same time on the same tile  
        '''
        for instile in self.instile_dict:
            if tile_id == instile:
                self.instile_dict[instile].charges.append(charge)
            else:
                self.instile_dict[instile].charges.append(self.NO_Q)
    
            self.instile_dict[instile].time_stamps.append(self.ts)


    def assemble_charge_and_time_lists(self,
                                       selection):
        ''' Assembles instile lists for charge and time '''
        # assemble bin edges for charge and time
        while self.ts < self.event_end_time:
            
            # just need to check if there's a timestep here and evaluate
            if self.ts == self.event_hits[self.hit_count][3]:

                _tile_id = selection.get_tile_id(self.event_hits[self.hit_count])
                self.append_charge_and_time(_tile_id,
                                            self.event_hits[self.hit_count][4]) 
                self.hit_count += 1

            else:
                self.ts += self.time_step



    def obtain_event_pulses(self,
                            selection):
        ''' Attempts to find pulses in an event '''
        self.reinitialize()
        self.event_start_time = self.event_hits[0][3]
        self.event_end_time   = self.event_hits[-1][3]
        self.ts               = self.event_start_time
        self.instile_dict     = self.assemble_instile_dict() # dictionary of 16 instiles
        self.time_stamps      = []

        self.assemble_charge_and_time_lists(selection)

        # now we need to make it into a histogram

        


    def find_pulses(self,
                    selection):
        ''' Main driver of pulse scanning '''
        cut_events = selection.get_cut_events()
        start_time = time.time()

        for evid in cut_events.keys():
            print('evaluating event {}'.format(evid))
            self.event      = selection.get_event(evid)
            self.event_hits = selection.get_event_hits(self.event)
            event_pulses    = self.obtain_event_pulses(selection)
        
        end_time = time.time()
        print('scan for pulses completed in {} seconds'.format(end_time - start_time))
        
