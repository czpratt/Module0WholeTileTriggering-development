import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from instile import Instile
from selection import Selection

matplotlib.rcParams['text.usetex'] = True

class PulseDisplay:
    ''' 
        Class for displaying pulses 
        ==> moving away from functional-based displaying
        NOTES:
            1) Can eventually turn this into a menu-esque system
            2) only utilizing LSB-related info for plots
            
    '''
    def __init__(self,
                 event_pulses,
                 q_thresh,
                 delta_time_slice):
        ''' Initialization '''
        self.event_pulses     = event_pulses
        self.q_thresh         = q_thresh
        self.delta_time_slice = delta_time_slice
         
        self.evid       = None
        self.event      = None
        self.event_hits = None
        self.tile_id    = None
   
        self.ts         = None
        self.hit_count  = None

        self.instile    = None

        self.time_stamps = None
        self.charges     = None
        self.rms         = None

        self.pulse_charges     = None
        self.pulse_time_stamps = None
    
        self.time_range = None
        self.event_start_ts = None
        self.event_end_ts   = None
        
        self.peak_charge_value = None
        self.peak_charge_value_ts = None

        

    def set_evid(self,
                 evid):
        ''' Sets evid for displaying '''
        self.evid = evid

    
    def set_event_hits(self,
                       selection):
        ''' Sets event hits '''
        self.event_hits = selection.get_event_hits(selection.get_event(self.evid))


    def set_tile_id(self,
                    tile_id):
        ''' Sets tile id for displaying '''
        self.tile_id = tile_id

    
    def set_instile(self,
                    instile):
        ''' Sets instile for displaying '''
        self.instile = instile

    
    def set_ts(self,
               ts):
        ''' Sets time stamp iterator '''
        self.ts = ts


    def set_hit_count(self,
                      hit_count):
        ''' Sets hit count iterator '''
        self.hit_count = hit_count

        
    def set_pulse_time_stamps(self,
                              pulse_id):
        ''' Sets time stamps of the pulse '''
        self.pulse_time_stamps = list(self.instile.time_stamps_list[pulse_id])


    def set_pulse_charges(self,
                          pulse_id):
        ''' Sets charges of pulse '''
        self.pulse_charges = list(self.instile.charges_list[pulse_id])

    
    def set_time_range(self,
                       time_range):
        ''' Sets full plotting range in time '''
        self.time_range = time_range

    
    def set_event_start_time_stamp(self):
        ''' Sets event start time stamp '''
        self.event_start_ts = self.event_hits[0][3]


    def set_event_end_time_stamp(self):
        ''' Sets event end time stamp '''
        self.event_end_ts = self.event_hits[-1][3]


    def get_nbins_by_lsb(self):
        ''' Fetches nbins by lsb '''
        return int(self.pulse_time_stamps[-1] - self.pulse_time_stamps[0])


    def obtain_peak_charge_info(self,
                                pulse_id):
        ''' Returns desired peak information of a pulse '''
        # peak charge value information (based on time slice)
        _peak_charge_value = round(self.instile.peak_charge_value_list[pulse_id], 2)
        _peak_charge_value_time_stamp = self.instile.peak_charge_value_time_stamp_list[pulse_id]
        
        # (based on collected hit information)
        _peak_charge_index     = self.pulse_charges.index(max(self.pulse_charges))
        _ts_at_peak_charge     = self.pulse_time_stamps[_peak_charge_index]
        
        _peak_range_difference = _ts_at_peak_charge - self.time_range
        _peak_range_addition   = _ts_at_peak_charge + self.time_range

        # obtain plot ranges
        _plot_range_start = self.event_start_ts if _peak_range_difference < self.event_start_ts \
                            else _peak_range_difference
        _plot_range_end   = self.event_end_ts if _peak_range_addition > self.event_end_ts \
                            else _peak_range_addition 
        
        _plot_range = _plot_range_end - _plot_range_start


        return _plot_range_start, _plot_range_end, _peak_charge_value, _ts_at_peak_charge


    def plot_charge_around_pulse_by_lsb(self,
                                        selection):
        ''' Plots charge that surrounds pulse '''
        _charges     = []
        _time_stamps = []
        _range = 75
        _hit_range = 10
        
        self.set_time_range(_range)
        
        # obtain charges and time_stamps surrounding hits
        for pulse in range(0, self.instile.npulse_count, 1):
            self.set_pulse_time_stamps(pulse)
            self.set_pulse_charges(pulse)
            self.set_hit_count(self.instile.first_hit_at_lsb_index[pulse])
            _nbins_lsb = self.get_nbins_by_lsb()
           
            # will eventually need a buffer here to we don't go out of bounds
            while self.hit_count < self.instile.last_hit_at_lsb_index[pulse] + _hit_range:
                _tile_id = selection.get_tile_id(self.event_hits[self.hit_count])
                if _tile_id == self.tile_id:
                    _time_stamps.append(self.event_hits[self.hit_count][3])
                    _charges.append(self.event_hits[self.hit_count][4])
                else:
                    # hit happened at a different tile
                    pass
                self.hit_count += 1

            
            _range_start, _range_end, peak_q_value, _ts_at_peak_q = \
                                                                  self.obtain_peak_charge_info(pulse)

            _nbins_lsb = self.get_nbins_by_lsb()

            fig, axs = plt.subplots()
            axs.hist(_time_stamps,
                     weights=_charges,
                     bins=_nbins_lsb,
                     histtype='step',
                     label='binned')

            _title = 'Event {}, Tile {}, nbins = {}'.format(self.evid, self.tile_id, _nbins_lsb)

            axs.set_title(r'{}'.format(_title))
            axs.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]')
            axs.set_ylabel(r'charge [1000 * $10^3$ e]')
            axs.set_xlim(xmin=_range_start, xmax=_range_end)

            plt.show()



    def display_pulses(self,
                       selection):
        ''' Driver function for displaying pulses '''
        for evid in self.event_pulses: 
            self.set_evid(evid)
            self.set_event_hits(selection)
            self.set_event_start_time_stamp()
            self.set_event_end_time_stamp()

            for tile_id in self.event_pulses[self.evid]:
                self.set_tile_id(tile_id)
                self.set_instile(self.event_pulses[self.evid][self.tile_id])
                
                self.plot_charge_around_pulse_by_lsb(selection)
