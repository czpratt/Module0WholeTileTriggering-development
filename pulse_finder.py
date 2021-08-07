''' ******************************************
    Attempts to find pulses in specific events
    ****************************************** '''

from selection import Selection
from collections import deque
from collections import Counter
from dataclasses import dataclass
from scipy.spatial import ConvexHull
import time
import numpy as np


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


class EventChargeWindows:
    ''' Event charge windows initiated as FIFO stacks for each tile  '''
    def __init__(self):
        self.window_1  = None 
        self.window_2  = None 
        self.window_3  = None 
        self.window_4  = None 
        self.window_5  = None 
        self.window_6  = None 
        self.window_7  = None 
        self.window_8  = None 
        self.window_9  = None 
        self.window_10 = None 
        self.window_11 = None 
        self.window_12 = None 
        self.window_13 = None 
        self.window_14 = None 
        self.window_15 = None 
        self.window_16 = None 
        
        self.window_pulse_start_1  = None
        self.window_pulse_start_2  = None
        self.window_pulse_start_3  = None
        self.window_pulse_start_4  = None
        self.window_pulse_start_5  = None
        self.window_pulse_start_6  = None
        self.window_pulse_start_7  = None
        self.window_pulse_start_8  = None
        self.window_pulse_start_9  = None
        self.window_pulse_start_10 = None
        self.window_pulse_start_11 = None
        self.window_pulse_start_12 = None
        self.window_pulse_start_13 = None
        self.window_pulse_start_14 = None
        self.window_pulse_start_15 = None
        self.window_pulse_start_16 = None
        
        self.all_windows          = None
        self.all_pulse_indicators = None
        self.pulse_count          = None
        self.startup()

    
    def __repr__(self):
        return ('{}'.format(self.all_windows))
    

    def startup(self):
        ''' 
            Initializes all windows as empty stacks,
            list of all windows,
            and pulse start indicators 
        '''
        self.window_1  = deque() 
        self.window_2  = deque() 
        self.window_3  = deque() 
        self.window_4  = deque() 
        self.window_5  = deque() 
        self.window_6  = deque() 
        self.window_7  = deque() 
        self.window_8  = deque() 
        self.window_9  = deque() 
        self.window_10 = deque() 
        self.window_11 = deque() 
        self.window_12 = deque() 
        self.window_13 = deque() 
        self.window_14 = deque() 
        self.window_15 = deque() 
        self.window_16 = deque()
        
        self.all_windows = [] 
        self.all_windows.append(self.window_1) 
        self.all_windows.append(self.window_2) 
        self.all_windows.append(self.window_3) 
        self.all_windows.append(self.window_4) 
        self.all_windows.append(self.window_5) 
        self.all_windows.append(self.window_6) 
        self.all_windows.append(self.window_7) 
        self.all_windows.append(self.window_8) 
        self.all_windows.append(self.window_9) 
        self.all_windows.append(self.window_10) 
        self.all_windows.append(self.window_11) 
        self.all_windows.append(self.window_12) 
        self.all_windows.append(self.window_13) 
        self.all_windows.append(self.window_14) 
        self.all_windows.append(self.window_15) 
        self.all_windows.append(self.window_16) 
        
        self.pulse_start_1  = False 
        self.pulse_start_2  = False
        self.pulse_start_3  = False
        self.pulse_start_4  = False
        self.pulse_start_5  = False
        self.pulse_start_6  = False
        self.pulse_start_7  = False
        self.pulse_start_8  = False
        self.pulse_start_9  = False
        self.pulse_start_10 = False 
        self.pulse_start_11 = False
        self.pulse_start_12 = False
        self.pulse_start_13 = False
        self.pulse_start_14 = False
        self.pulse_start_15 = False
        self.pulse_start_16 = False
    

    def check_length(self, 
                     max_length):
        ''' Verifies length of window '''
        for window in self.all_windows:
            if len(window) < max_length:
                pass
            else:
                window.popleft()


    def append_charges(self,
                       tile_id,
                       q):

        '''
            Appending charges to windows
            - if there's a tile_id match, append q
            - else append 0
            tile_count := counter iterating through all tiles
        '''
        tile_count = 1 # iterates through all tiles
        for window in self.all_windows:
            if tile_count == tile_id:
                window.append(q)
            else:
                window.append(0)
            
            tile_count += 1
    
        
    def set_pulse_start(self,
                        tile_id,
                        decision):
        ''' Change the bool value based on tile_id '''
        try:
            if tile_id == 1:
                self.pulse_start_1 = decision
            elif tile_id == 2:
                self.pulse_start_2 = decision
            elif tile_id == 3:
                self.pulse_start_3 = decision
            elif tile_id == 4:
                self.pulse_start_4 = decision
            elif tile_id == 5:
                self.pulse_start_5 = decision
            elif tile_id == 6:
                self.pulse_start_6 = decision
            elif tile_id == 7:
                self.pulse_start_7 = decision
            elif tile_id == 8:
                self.pulse_start_8 = decision
            elif tile_id == 9:
                self.pulse_start_9 = decision
            elif tile_id == 10:
                self.pulse_start_10 = decision
            elif tile_id == 11:
                self.pulse_start_11 = decision
            elif tile_id == 12:
                self.pulse_start_12 = decision
            elif tile_id == 13:
                self.pulse_start_13 = decision
            elif tile_id == 14:
                self.pulse_start_14 = decision
            elif tile_id == 15:
                self.pulse_start_15 = decision
            elif tile_id == 16:
                self.pulse_start_16 = decision
            
        except:
            print('ERROR: NO TILE_ID FOUND')



class PulseFinder:
    ''' Class for finding pulses within a TPC waveform '''
    def __init__(self, 
                 time_step: int,
         	     q_thresh: int,
         	     max_q_window_len: int, 
         	     datalog_file: str,
         	     geometry_file: str):

        self.time_step            = time_step         # passed time step
        self.q_thresh             = q_thresh          # charge threshold
        self.max_q_window_length  = max_q_window_len  # max charge window length
        self.q_window             = deque() # initializing tpc1 charge window stack
        self.hit_count            = 0       # keeps track of hits in event
        self.event_start_time     = None    # event start time (detector time)
        self.event_end_time       = None    # event end time (detector time)
        self.tile                 = None    # tile
        self.event                = None    # individual event
        self.hit_ref              = None    # intermediate step
        self.event_hits           = None    # all hits within event
        self.candidate_pulses     = None    # candidate pulse storage
        self.event_pulses         = None
        self.tile_pulses          = None
        self.all_pulses           = {}
        self.npulses_on_tiles     = None    # keeps track of how many 

    def create_pulse(self, 
                     tile_id, 
                     event_id,
                     event_pulse_array):
        '''
            creates Pulse instance with PulseFinder information
            --> see Pulse dataclass for variable descriptions
            event_pulse_array contains: 
            [tile id, hit_id, timestamp, sum of charge in window]
        '''
        hit_start_time   = event_pulse_array[0][1]
        hit_end_time     = event_pulse_array[-1][1]
        pulse_start_time = event_pulse_array[0][2]
        pulse_end_time   = event_pulse_array[-1][2]
        delta_t          = pulse_end_time - pulse_start_time 
        peak_q           = max(map(lambda q: q[3], event_pulse_array))  
        total_q          = sum(map(lambda q: q[3], event_pulse_array))
        temp_array       = np.array(event_pulse_array) 
        peak_q_index     = np.where(temp_array == peak_q)
        peak_q_hit_id    = event_pulse_array[peak_q_index[0][0]][1]
        peak_q_hit       = next(
                           filter(
                           lambda hit: hit[0] == peak_q_hit_id, self.event_hits), None)
        peak_q_hit_x     = peak_q_hit[1]
        peak_q_hit_y     = peak_q_hit[2]
        peak_q_hit_ts    = peak_q_hit[3]
        hit_positions    = [[hit[1], hit[2]] for hit in self.event_hits]
        pulse_area       = ConvexHull(hit_positions).volume
        
        pulse = Pulse(event_id,  
                      tile_id,
                      hit_start_time, 
                      hit_end_time, 
                      pulse_start_time, 
                      pulse_end_time, 
                      delta_t, 
                      total_q, 
                      peak_q, 
                      peak_q_hit_id, 
                      peak_q_hit_ts, 
                      peak_q_hit_x, 
                      peak_q_hit_y, 
                      pulse_area)
        
        if tile_id not in self.tile_pulses:
            self.tile_pulses[tile_id] = []
        
        self.tile_pulses[tile_id].append(pulse)


    def inspect_tile_for_pulses(self,
                                pulse_start,
                                q_window,
                                q_thresh,
                                eqw,
                                tile_id,
                                hc):

        ''' Inspect individual tile to see if a pulse was found '''
        if sum(q_window) > q_thresh and pulse_start == False:
            # a new pulse was found, 
            # store as an event pulse
            eqw.set_pulse_start(tile_id, True)
            self.candidate_pulses[tile_id] = [[tile_id, self.event_hits[hc][0], self.event_hits[hc][3], sum(q_window)]]


        elif sum(q_window) > q_thresh and pulse_start == True:
            self.candidate_pulses[tile_id].append([tile_id, self.event_hits[hc][0], self.event_hits[hc][3], sum(q_window)])


        elif sum(q_window) < q_thresh and pulse_start == True:
            eqw.set_pulse_start(tile_id, False)
            self.create_pulse(tile_id, self.event[0], self.candidate_pulses[tile_id]) 
            self.npulses_on_tiles[tile_id] += 1

            try:
                del self.candidate_pulses[tile_id]
            except:
                print('CANDIDATE PULSE NOT FOUND')


        else:
            # no pulse was found, do nothing
            pass



    def make_pulse_determination(self, 
                                 eqw,
                                 hc):

        ''' 
        Determine if a pulse was found at every charge window 
        * currently set up this way so class variables update accordingly
        - eqw = event charge window
        - hc  = hit count
        '''
        self.inspect_tile_for_pulses(eqw.pulse_start_1, eqw.window_1, self.q_thresh, eqw, 1, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_2, eqw.window_2, self.q_thresh, eqw, 2, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_3, eqw.window_3, self.q_thresh, eqw, 3, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_4, eqw.window_4, self.q_thresh, eqw, 4, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_5, eqw.window_5, self.q_thresh, eqw, 5, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_6, eqw.window_6, self.q_thresh, eqw, 6, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_7, eqw.window_7, self.q_thresh, eqw, 7, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_8, eqw.window_8, self.q_thresh, eqw, 8, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_9, eqw.window_9, self.q_thresh, eqw, 9, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_10, eqw.window_10, self.q_thresh, eqw, 10, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_11, eqw.window_11, self.q_thresh, eqw, 11, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_12, eqw.window_12, self.q_thresh, eqw, 12, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_13, eqw.window_13, self.q_thresh, eqw, 13, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_14, eqw.window_14, self.q_thresh, eqw, 14, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_15, eqw.window_15, self.q_thresh, eqw, 15, hc) 
        self.inspect_tile_for_pulses(eqw.pulse_start_16, eqw.window_16, self.q_thresh, eqw, 16, hc) 


    def initialize_candidate_pulses(self):
        ''' Initialization of necessary criteria '''
        self.candidate_pulses = {}
        self.event_pulses = {}
        self.tile_pulses = {}
        self.npulses_on_tiles  = {i:0 for i in range(1, 16 + 1)}


    def make_cut_on_npulses_per_tile(self):
        ''' Make final cut to ensure this isn't a sync pulse '''
        cut_list = {key:val for key, val in self.npulses_on_tiles.items() if val != 0}
        
        if len(cut_list) > 7:
            pass
        else:
            print('o-- potential WTT event at {} --o'.format(self.event[0]))
            self.all_pulses[self.event[0]] = self.event_pulses
    
    
    
    def obtain_event_pulses(self,
                            selection):
        ''' Finds pulses within cut events '''
        self.event_start_time = self.event_hits[0][3]
        self.event_end_time   = self.event_hits[-1][3]
        ts                    = self.event_start_time
        event_q_windows       = EventChargeWindows()
        hit_count = self.hit_count
        self.initialize_candidate_pulses()
        
        while ts < self.event_end_time:
                
            # validate length of charge windows
            event_q_windows.check_length(self.max_q_window_length)
            
            if ts == self.event_hits[hit_count][3]:
                # a hit was found, get hit's tile location,
                # append to stack
                _tile_id = selection.get_tile_id(self.event_hits[hit_count])
                event_q_windows.append_charges(_tile_id, 
                                               abs(self.event_hits[hit_count][4])) 
                
                # determine whether there was a pulse at each tile
                self.make_pulse_determination(event_q_windows, 
                                              hit_count)

                # append hit count since a hit was found
                hit_count += 1

            else:
                ts += self.time_step

        # analyze pulses on tile dictionary at the end
        #self.make_cut_on_npulses_per_tile()
        


    def find_pulses(self, 
                    selection):
        ''' Drives pulse finding '''
        cut_events = selection.get_cut_events()
        start_time = time.time()
       
        for evid in cut_events.keys():
            print('evaluating event {}'.format(evid))
            self.event      = selection.get_event(evid)
            self.event_hits = selection.get_event_hits(self.event)
            self.obtain_event_pulses(selection) 
            self.event_pulses[evid] = self.tile_pulses
            self.tile_pulses = {}


        end_time = time.time()
        #print(self.event_pulses)
        print('scan for pulses completed in {} seconds'.format(end_time - start_time))
        print('all potential WTT events: {}'.format(self.event_pulses.keys()))
    
        return self.event_pulses

        ''' Big note:
            -- Multiple hits can be logged at the same time
		AKA multiple 'pulses' can be actual hits that are below charge 
		are logged on the tile, potentially triggering the end of a pulse '''

        
