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

        self.pulse_charges     = None
        self.pulse_time_stamps = None
    
        self.time_range = None
        self.event_start_ts = None
        self.event_end_ts   = None
        
        self.peak_charge_value = None
        self.peak_charge_value_ts = None
        self.rms = None


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
                      first_hit_at_lsb,):
        ''' Sets hit count iterator '''
        self.hit_count = 0
        
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


    def set_peak_charge_value(self,
                              pulse_id):
        ''' Sets value of the charge at the peak of pulse '''
        self.peak_charge_value = round(self.instile.peak_charge_value_list[pulse_id], 2)

        
    def set_peak_charge_value_time_stamp(self,
                                         pulse_id):
        ''' Sets time stamp of the pulses's peak charge value '''
        self.peak_charge_value_time_stamp = self.instile.peak_charge_value_time_stamp_list[pulse_id]


    def set_rms(self):
        ''' Sets rms value of current pulse '''
        _pulse_start_time = self.pulse_time_stamps[0]
        _pulse_end_time   = self.pulse_time_stamps[-1]
        
        _normalized_time_stamps = np.array(self.pulse_time_stamps - _pulse_start_time)
        _rms = round(np.sqrt(np.mean(_normalized_time_stamps) ** 2), 2)    

        self.rms = _rms


    def obtain_nbins(self,
                     time_stamps):
        ''' 
            Fetches nbins by lsb and time slice
            NOTES:
                (1) Come up with better naming schemes
        '''
        _cut_time_stamps = sorted(list(set(time_stamps)))
        _nbins_lsb = (_cut_time_stamps[-1] - _cut_time_stamps[0])
        _nbins_time_slice = int(_nbins_lsb / self.delta_time_slice)
        _nbins_limit_time_slice = int(math.ceil(_nbins_time_slice / self.delta_time_slice))

        return _nbins_lsb, _nbins_time_slice, _nbins_limit_time_slice
        

    def obtain_peak_charge_info(self,
                                pulse_id):
        ''' Returns desired peak information of a pulse '''
        self.set_peak_charge_value(pulse_id)
        self.set_peak_charge_value_time_stamp(pulse_id)
        
        _peak_range_difference = self.peak_charge_value_time_stamp - self.time_range
        _peak_range_addition   = self.peak_charge_value_time_stamp + self.time_range

        # obtain plot ranges
        _plot_range_start = self.event_start_ts if _peak_range_difference < self.event_start_ts \
                            else _peak_range_difference
        _plot_range_end   = self.event_end_ts if _peak_range_addition > self.event_end_ts \
                            else _peak_range_addition 

        return _plot_range_start, _plot_range_end


    def plot_charge_around_pulse_by_lsb(self,
                                        selection):
        ''' Plots charge that surrounds pulse '''
        _charges     = []
        _time_stamps = []
        _range = 250        # temporary
        _hit_range = 100

        #self.set_time_range(_range)
        
        # obtain charges and time_stamps surrounding hits
        for pulse in range(0, self.instile.npulse_count, 1):
            self.set_pulse_time_stamps(pulse)
            self.set_pulse_charges(pulse)
            self.set_hit_count(self.instile.first_hit_at_lsb_index[pulse])
            self.set_rms()

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

            
            _nbins_lsb, _nbins_time_slice, _nbins_limit_time_slice = self.obtain_nbins(_time_stamps)

            self.set_time_range(_range)

            _range_start, _range_end = self.obtain_peak_charge_info(pulse)
    
            ''' Plot 1: # of LSB increments '''
            fig, (axs, axs_info) = plt.subplots(1, 2)
            
            axs.hist(_time_stamps,
                     weights=_charges,
                     bins=_nbins_lsb,
                     histtype='step',
                     label='binned')

            _title = 'Event {}, Tile {}'.format(self.evid, self.tile_id)

            axs.set_title(r'{}'.format(_title))
            axs.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]', loc='left')
            axs.set_ylabel(r'charge [1000 * $10^3$ e]', loc='bottom')
            axs.set_xlim(xmin=_range_start, xmax=_range_end)
          
            axs_info_test = '''1 bin := 1 LSB increment
                               plot\_range = {}
                               rms = {} 
                               peak charge value = {}
                               peak charge value ts = {}
                            '''.format(_range_end - _range_start,
                                       self.rms,
                                       self.peak_charge_value,
                                       self.peak_charge_value_time_stamp)

            axs_info.text(0.1, 0.60, axs_info_test, transform=axs_info.transAxes, fontsize=11, verticalalignment='top')
            axs_info.set_xticklabels([])
            axs_info.set_yticklabels([])
            axs_info.set_xticks([])
            axs_info.set_yticks([])

            ''' Plot 2: # of sliding window entries ''' 
            fig2, (ax2, ax2_info) = plt.subplots(1, 2) 
            ax2.hist(_time_stamps,
                     weights=_charges,
                     bins=_nbins_time_slice,
                     histtype='step',
                     label='binned')
            _title_2 = 'Event {}, Tile {}'.format(self.evid, self.tile_id)

            ax2.set_title(r'{}'.format(_title_2))
            ax2.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]', loc='left')
            ax2.set_ylabel(r'charge [1000 * $10^3$ e]', loc='bottom')
            ax2.set_xlim(xmin=_range_start, xmax=_range_end)
          
            ax2_info_test = '''1 bin := 1 sliding window element  
                               plot\_range = {}
                               rms = {} 
                               peak charge value = {}
                               peak charge value ts = {}
                            '''.format(_range_end - _range_start,
                                       self.rms,
                                       self.peak_charge_value,
                                       self.peak_charge_value_time_stamp)

            ax2_info.text(0.1, 0.60, ax2_info_test, transform=ax2_info.transAxes, fontsize=11, verticalalignment='top')

            ax2_info.set_xticklabels([])
            ax2_info.set_yticklabels([])
            ax2_info.set_xticks([])
            ax2_info.set_yticks([])

            ''' Plot 3: 5 sliding window entries per bin (25 LSB's) '''
            fig3, (ax3, ax3_info) = plt.subplots(1, 2)
            ax3.hist(_time_stamps,
                     weights=_charges,
                     bins=_nbins_limit_time_slice,
                     histtype='step',
                     label='binned')

            _title_3 = 'Event {}, Tile {}'.format(self.evid, self.tile_id)

            ax3.set_title(r'{}'.format(_title_3))
            ax3.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]', loc='left')
            ax3.set_ylabel(r'charge [1000 * $10^3$ e]', loc='bottom')
            ax3.set_xlim(xmin=_range_start, xmax=_range_end)
          
            ax3_info_test = '''1 bin := 5 sliding window elements 
                               plot\_range = {}
                               rms = {} 
                               peak charge value = {}
                               peak charge value ts = {}
                            '''.format(_range_end - _range_start,
                                       self.rms,
                                       self.peak_charge_value,
                                       self.peak_charge_value_time_stamp)

            ax3_info.text(0.1, 0.60, ax3_info_test, transform=ax3_info.transAxes, fontsize=11, verticalalignment='top')

            ax3_info.set_xticklabels([])
            ax3_info.set_yticklabels([])
            ax3_info.set_xticks([])
            ax3_info.set_yticks([])

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
