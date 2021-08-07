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
        
        self.window      = None     # charge window
        self.charges     = None     # list of charges from hits
        self.time_stamps = None     # list of time stamps of hits
        self.histogram   = None     # placeholder for tile histogram
        self.q_edges     = None     # placeholder for charge edges for histogram
        self.t_edges     = None     # placeholder for time edges for histogram
        
        self.startup()
    
    
    def startup(self):
        ''' Initialization for redundancy '''
        self.window      = deque()
        self.charges     = []
        self.time_stamps = []


    def __repr__(self):
        ''' String representation function '''
        return ('window: {}, charges = {}, time stamps = {}\n'.format(self.window,
                                                                      self.charges,
                                                                      self.time_stamps))
    
    def set_histogram(self,
                      histogram):
        ''' Sets histogram for the tile '''
        self.histogram = histogram


    def set_q_edges(self,
                    q_edges):
        ''' Sets histogram edges for charge '''
        self.q_edges = q_edges

    
    def set_t_edges(self,
                    t_edges):
        ''' Sets histogram edges for time stamps '''
        self.t_edges = t_edges
   

    def get_histogram(self):
        ''' Getter for histogram '''
        return self.histogram


    def get_q_edges(self):
        ''' Getter for charge edges for histogram '''
        return self.q_edges


    def get_t_edges(self):
        ''' Getter for time stamp edges for histogram '''
        return self.t_edges


    def set_pulse_indicator(self,
                            decision):
        ''' Sets the pulse indicator '''
        self.pulse_indicator = decision


    def check_window_length(self):
        ''' Verifies length of window '''
        if len(self.window) < self.max_q_window_len:
            pass
        else:
            self.window.popleft()



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

        self.event      = None      # analyzed event
        self.hits       = None      # hits of analyzed event
        self.event_hits = None      # hits specific to event
        self.hit_count  = None      # hit counter for keeping track of iteration
        self.instile_dict = None    # dictionary of instiles
        
        self.NO_HIT = -10       # constant for when no hit occurred
        self.NO_Q   = 0         # constant for when no charge
        
        self.event_start_time = None
        self.event_end_time   = None
        


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


    def plot_histograms(self):
        ''' 
            Makes histograms
            --> will probably need to adjust bin size!
            NOTES:
                1) will need to loop if there are multiple tiles 
        ''' 
        nbins = 500
        fig, axs = plt.subplots()
         
        print('min time_stamp: {}'.format(min(self.instile_dict[7].time_stamps)))
        print('max time_stamp: {}'.format(max(self.instile_dict[7].time_stamps)))
        print('min charge: {}'.format(min(self.instile_dict[7].charges)))
        print('max charge: {}'.format(max(self.instile_dict[7].charges)))
        
        # 2D color norms are weird
        '''
        axs.hist2d(self.instile_dict[7].time_stamps,
                   self.instile_dict[7].charges,
                   bins=nbins)
        '''
        axs.hist(self.instile_dict[2].time_stamps,
                 weights=self.instile_dict[2].charges,
                 bins=nbins,
                 histtype='step', 
                 label='binned')
        
        axs.set_title('Tile 2, Event {}'.format(self.event[0]))
        axs.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]')
        axs.set_ylabel(r'charge [1000 * $10^3$ e]')

        plt.show()
   
    
    def make_histogram_data(self):
        ''' Making histogram data for pulse finding 
        ---> most likely a temporary function '''
        
        # temporary testing
        charges = self.instile_dict[7].charges
        times   = self.instile_dict[7].time_stamps
        nbins   = 500

        charges_test = self.instile_dict[1].charges
        times_test   = self.instile_dict[1].time_stamps

        #match = charges == charges_test
        #print('match: {}'.format(match))

        hist = None
        t_edges = None
        q_edges = None

        hist, t_edges, q_edges = np.histogram2d(times, charges, bins=nbins)
        
        #print('hist: {}'.format(hist))
        print('t_edges: {}'.format(t_edges))
        print('q_edges: {}'.format(q_edges))
        
        plt.imshow(hist, extent=[t_edges[0], t_edges[-1], q_edges[0], q_edges[-1]])
        plt.show()

    def obtain_event_pulses(self,
                            selection):
        ''' Attempts to find pulses in an event '''
        # here we would then activate the pulse finding algorithm
        # Mike wants this done over the bins of the made histogram, 
        # however it's not working well right now.....
        
        #self.make_histogram_data()

        # set up histograms for the tiles
        # --> maybe this is where to utilize the bins in order to set up the 
        #    charge window? also need to figure out color norm lol
        self.plot_histograms() 




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
            self.assemble_charge_and_time_lists(selection)    
             
            event_pulses       = self.obtain_event_pulses(selection)
        
        end_time = time.time()
        print('scan for pulses completed in {} seconds'.format(end_time - start_time))
