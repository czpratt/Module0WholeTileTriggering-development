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

from instile import Instile
from selection import Selection

matplotlib.rcParams['text.usetex'] = True   # for LaTeX font on tile plots


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

        self.event         = None      # analyzed event
        self.hits          = None      # hits of analyzed event
        self.event_hits    = None      # hits specific to event
        self.hit_count     = None      # hit counter for keeping track of iteration
        self.instile_dict  = None    # dictionary of instiles

        self.event_start_time = None
        self.event_end_time   = None
        self.max_time_step    = None   # maximum attainable time slice
        
        self.tile_pulses      = None   # keeps track of npulses on a tile
        
        self.NO_HIT                = -10    # constant for when no hit occurred
        self.NO_Q                  = 0      # constant for when no charge
        self.SYNC_PULSE_CONSTRAINT = 8      # ntile value for sync pulse classification

        self.first_hit_at_lsb_index = None
        self.first_hit_at_lsb_flag = None


    def assemble_instile_dict(self):
        ''' Creates dictionary of charge windows for each tile '''
        instile_dict = {}
        for tile in range(1, self.nwindows + 1, 1):
            instile = Instile(self.max_q_window_len,
                              self.q_thresh,
                              tile)
    
            instile_dict[tile] = instile
    
        return instile_dict


    def reinitialize(self):
        ''' Reinitialization of certain variables '''
        self.instile_dict     = None
        self.event_start_time = None
        self.event_end_time   = None
        self.time_stamps      = None
        self.ts               = None
        self.first_hit_at_lsb_index = 0
        self.first_hit_at_lsb_flag  = None
        self.hit_count        = 0
        self.max_time_step    = 0
        
        self.tile_pulses     = {}
        self.complete_pulses = {}
        self.event_pulses    = {}


    def append_charge_and_time(self,
                               tile_id,
                               time_stamp,
                               charge):
        ''' Appending instile charge and timestamp lists post processing '''
        self.instile_dict[tile_id].time_stamps.append(time_stamp)
        self.instile_dict[tile_id].charges.append(charge)


    def assemble_charge_and_time_lists(self):
        ''' Assembles instile lists for charge and time for pulse finding '''
        # iterating through tiles that logged a pulse
        for tile_id in self.tile_pulses:
            
            # iterating through all logged pulses
            for i in range (0, len(self.instile_dict[tile_id].pulse_start_time_stamp), 1):
                _pulse_start_time = self.instile_dict[tile_id].pulse_start_time_stamp[i]
                _pulse_end_time   = self.instile_dict[tile_id].pulse_end_time_stamp[i]
                _hit_index        = self.instile_dict[tile_id].first_hit_at_lsb_index[i]
                _ts               = _pulse_start_time
                
                # iterate until the end of the pulse
                while _ts < _pulse_end_time:
                     
                    if _ts == self.event_hits[_hit_index][3]:
                        # a match, 
                        # append charge and associated time stamp to instile deque
                        self.append_charge_and_time(tile_id,
                                                    _ts,
                                                    self.event_hits[_hit_index][4])
                        _hit_index += 1
                   
                    else:
                        _ts += self.time_step

           
            # store charges and timestamps stacks into list once completed
            self.instile_dict[tile_id].store_charges_in_list()
            self.instile_dict[tile_id].store_time_stamps_in_list()

            # store completed pulses in event per instile
            if tile_id not in self.complete_pulses:
                self.complete_pulses[tile_id] = {}

            self.complete_pulses[tile_id] = self.instile_dict[tile_id]


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
        ''' Clears all instile charge windows '''
        for instile in self.instile_dict:
            self.instile_dict[instile].window.clear()


    def make_pulse_determination(self):
        ''' 
            Determines whether a pulse was found or not, and 
            stores values accordingly
        '''
        for instile in self.instile_dict:
            _sum_window = sum(self.instile_dict[instile].window)
            _start_indicator = self.instile_dict[instile].pulse_indicator

            if self.q_thresh < _sum_window and _start_indicator == False:
                #print('beginning of a pulse was found at tile {}, ts = {}'.format(instile, self.ts))
                self.instile_dict[instile].set_pulse_indicator(True)
                self.instile_dict[instile].set_pulse_start_time_stamp(self.ts - self.delta_time_slice)
                self.instile_dict[instile].set_first_hit_at_lsb_index(self.first_hit_at_lsb_index)  
                self.instile_dict[instile].increment_npulse_count()
                
                # add to tile_pulses to keep track
                self.tile_pulses[instile] = self.instile_dict[instile].get_npulse_count()


            elif self.q_thresh < _sum_window and _start_indicator == True:
                # do nothing since there's nothing to do
                pass


            elif self.q_thresh > _sum_window and _start_indicator == True:
                #print('end of a pulse was found at {}, ts = {}'.format(instile, self.ts))
                self.instile_dict[instile].set_pulse_indicator(False)
                self.instile_dict[instile].set_pulse_end_time_stamp(self.ts)
               


    def sync_pulse_determination(self):
        ''' Determine if pulses within an event are related to syncing '''
        if len(self.tile_pulses) > self.SYNC_PULSE_CONSTRAINT:
            print('********************************************')
            print('* event {} is most likely a sync pulse,'.format(self.event[0]))
            print('* containing {} tiles that had a \'pulse\''.format(len(self.tile_pulses)))
            print('********************************************')
        else:
            print('o-----------------------------------------o')
            print('event {} does not contain a sync pulse'.format(self.event[0]))
            print('o-----------------------------------------o')
            self.assemble_charge_and_time_lists()



    def obtain_event_pulses(self,
                            selection):
        ''' Attempts to find pulses in an event '''
        while self.ts < self.event_end_time:
            
            # determine max timestep and determine if we'd still be in the
            # time range of an event
            self.max_time_step = self.ts + self.delta_time_slice 

            # now iterate through the time slice
            while self.ts < self.max_time_step:
             
                # end case,
                # ensures a constrained iteration
                if self.hit_count == len(self.event_hits):
                    self.ts = self.event_end_time
                    break

                # otherwise check if there's a time stamp within time slice
                if self.ts == self.event_hits[self.hit_count][3]:
                    # a hit was found within the timing window,
                    # obtain tile location and append to stack
                    # -- check if this is the first hit found by lsb
                    if self.first_hit_at_lsb_flag == False:
                        self.first_hit_at_lsb_index = self.hit_count
                        self.first_hit_at_lsb_flag = True

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

            # reset all hit lsb information
            self.first_hit_at_lsb_index = 0
            self.first_hit_at_lsb_flag  = False

        # concluded looping through event,
        # determine if this was a sync pulse or not
        self.sync_pulse_determination()
        

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
            
            self.obtain_event_pulses(selection)

            if self.complete_pulses:
                self.event_pulses[evid] = self.complete_pulses 
                print(self.event_pulses[evid]) 


        print(self.event_pulses)
        end_time = time.time()
        print('scan for pulses completed in {} seconds'.format(end_time - start_time))

