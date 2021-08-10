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
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['text.usetex'] = True   # for LaTeX font on tile plots

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


class TileSpike:
    ''' A specific 'spike' that happens on a pulse '''
    def __init__(self,
                 tile_id,
                 time_stamp):

        self.tile_id = tile_id
        self.spike_timestamp = time_stamp   # at spike's occurance





class Instile:
    ''' INformation Storage about a TILE 
        - self explanatory; stores information about a tile
          throughout an event, including its charge window, 
          and potential lists to be used for histograms         
         -- this will also handle prewindows, etc., eventually 
          
          '''
    def __init__(self,
                 max_q_window_len: int,
                 q_thresh: float):
                 
        self.max_q_window_len = max_q_window_len
        self.q_thresh         = q_thresh
        
        self.window          = None     # charge window
        self.pulse_indicator = None     # indicator for the start of a pulse 
        
        self.pulse_start_time_stamp = None
        self.pulse_end_time_stamp   = None

        self.charges     = None     # list of charges from hits
        self.time_stamps = None     # list of time stamps of hits
        
        self.histogram   = None     # placeholder for tile histogram
        
        self.startup()
    
    
    def startup(self):
        ''' Initialization for redundancy '''
        self.window          = deque()
        self.pulse_indicator = False
        self.charges         = []
        self.time_stamps     = []
        

    def __repr__(self):
        ''' String representation function '''
        return ('window: {}, charges = {}, time stamps = {}\n'.format(self.window,
                                                                      self.charges,
                                                                      self.time_stamps))
    
    def set_pulse_start_time_stamp(self,
                                   pulse_start_time):
        ''' Start time of the pulse '''
        self.pulse_start_time_stamp = pulse_start_time 

    
    def set_pulse_end_time_stamp(self,
                                 pulse_end_time):
        ''' Start time of the pulse '''
        self.pulse_end_time_stamp = pulse_end_time 



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
                 max_q_window_len: int,
                 delta_time_slice: int):

        self.nwindows          = n                    # number of windows/tiles
        self.time_step         = time_step            # timestep
        self.q_thresh          = q_thresh             # charge threshold
        self.max_q_window_len  = max_q_window_len     # maximum length of charge window
        self.delta_time_slice  = delta_time_slice     # time window for accumulating charge window

        print('self.max_q_window_len: {}'.format(self.max_q_window_len))

        self.max_time_step = None

        self.event      = None      # analyzed event
        self.hits       = None      # hits of analyzed event
        self.event_hits = None      # hits specific to event
        self.hit_count  = None      # hit counter for keeping track of iteration
        self.instile_dict = None    # dictionary of instiles
        
        self.NO_HIT = -10       # constant for when no hit occurred
        self.NO_Q   = 0         # constant for when no charge
        
        self.event_start_time = None
        self.event_end_time   = None
        
        self.tile_pulses = None
        self.npulses_on_tiles = None    # for later


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
        self.ts               = None
        self.hit_count        = 0
        self.max_time_step    = 0
        self.tile_pulses      = {}


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
            NOTES: 
                1) multiple hits can be logged at the same time on the same tile  
                2) logging absolute value of charge by convention
        '''
        for instile in self.instile_dict:
            if tile_id == instile and tile_id != self.NO_HIT:
                self.instile_dict[instile].charges.append(abs(charge))
            else:
                self.instile_dict[instile].charges.append(self.NO_Q)
    
            self.instile_dict[instile].time_stamps.append(self.ts)


    def assemble_charge_and_time_lists(self,
                                       selection):
        ''' Assembles instile lists for charge and time for pulse finding '''
        while self.ts < self.event_end_time:
            
            # just need to check if there's a timestep here and evaluate
            if self.ts == self.event_hits[self.hit_count][3]:

                _tile_id = selection.get_tile_id(self.event_hits[self.hit_count])
                self.append_charge_and_time(_tile_id,
                                            self.event_hits[self.hit_count][4]) 
                self.hit_count += 1

            else:
                self.append_charge_and_time(self.NO_HIT,
                                            self.NO_Q) 
                self.ts += self.time_step

   
    

    
    def check_instile_dict_lengths(self):
        ''' For prudence '''
        for instile in self.instile_dict:
            self.instile_dict[instile].check_window_length()


    def append_charge_windows(self,
                              tile_id,
                              charge):
        ''' Appends values to charge windows '''
        for instile in self.instile_dict:
            if tile_id == instile:
                self.instile_dict[instile].window.append(charge)
            else:
                self.instile_dict[instile].window.append(self.NO_Q)

    def clear_instile_windows(self):
        for instile in self.instile_dict:
            self.instile_dict[instile].window.clear()


    def make_pulse_determination(self):
        ''' Determines whether a pulse was found or not '''
        for instile in self.instile_dict:
            _sum_window = sum(self.instile_dict[instile].window)
            _start_indicator = self.instile_dict[instile].pulse_indicator

            if self.q_thresh < _sum_window and _start_indicator == False:
                print('beginning of a pulse was found at tile {}, ts = {}'.format(instile, self.ts))
                #print(self.instile_dict[instile].window)
                #print('len(window), _sum_window, indicator: {}, {}, {}'.format(len(self.instile_dict[instile].window), _sum_window, self.instile_dict[instile].pulse_indicator))
                self.instile_dict[instile].set_pulse_indicator(True)
                self.instile_dict[instile].set_pulse_start_time_stamp(self.ts - self.delta_time_slice)
                
                # then add this to the tile_pulses dictionary
                #self.tile_pulses[instile] = [[tile_]] 

            elif self.q_thresh < _sum_window and _start_indicator == True:
                #print('continuation of a pulse at tile {}, ts = {}'.format(instile, self.ts))
                #print('len(window), _sum_window, indicator: {}, {}, {}'.format(len(self.instile_dict[instile].window), _sum_window, self.instile_dict[instile].pulse_indicator))
                
                # do nothing since there's nothing to do
                pass


            elif self.q_thresh > _sum_window and _start_indicator == True:
                print('end of a pulse was found at {}, ts = {}'.format(instile, self.ts))
                self.instile_dict[instile].set_pulse_indicator(False)
                self.instile_dict[instile].set_pulse_end_time_stamp(self.ts)
                
                # create the pulse and store it here
                self.create_pulse(instile, 
                                  self.event[0],
                                  )


    def obtain_event_pulses(self,
                            selection):
        ''' Attempts to find pulses in an event '''
        
        # lasts throughout an event
        while self.ts < self.event_end_time:
            
            # determine max timestep and determine if we'd still be in the
            # time range of an event
            self.max_time_step = self.ts + self.delta_time_slice 

            if self.max_time_step > self.event_end_time:
                # completely break out of while loop,
                # done finding pulses
                break
            else:
                pass
            
            # now iterate through the time slice
            while self.ts < self.max_time_step:
                
                if self.ts == self.event_hits[self.hit_count][3]:
                    # a hit was found within the timing window,
                    # obtain tile location and append to stack
                    _tile_id = selection.get_tile_id(self.event_hits[self.hit_count])
                    _charge  = abs(self.event_hits[self.hit_count][4])
                    self.append_charge_windows(_tile_id,
                                               _charge)
                    self.hit_count += 1 

                else:
                    self.ts += self.time_step


            # once we're out of this loop, THEN we determine if a pulse
            # is within the time window or not
            self.make_pulse_determination() 
            
            # now clear the stack for the next iteration through time,
            # since at certain timestamps there can be many, many hits
            self.clear_instile_windows()


        # at the end of the loop


    def find_pulses(self,
                    selection):
        ''' Main driver of pulse scanning '''
        cut_events = selection.get_cut_events()
        start_time = time.time()

        for evid in cut_events.keys():
            print('evaluating event {}'.format(evid))
            # initialize and obtain information,
            # obtain pulses
            self.reinitialize()
            self.event      = selection.get_event(evid)
            self.event_hits = selection.get_event_hits(self.event)
            self.event_start_time = self.event_hits[0][3]
            self.event_end_time   = self.event_hits[-1][3]
            self.ts               = self.event_start_time
            self.instile_dict     = self.assemble_instile_dict() 
            self.time_stamps      = []
            
            event_pulses       = self.obtain_event_pulses(selection)
            
            # unnecessary now
            #self.assemble_charge_and_time_lists(selection)    
             
        

        end_time = time.time()
        print('scan for pulses completed in {} seconds'.format(end_time - start_time))
