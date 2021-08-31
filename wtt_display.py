import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from instile import Instile
from selection import Selection

matplotlib.rcParams['text.usetex'] = True

class WholeTileTriggerDisplay:
    ''' Class for displaying whole tile triggering events (pulses) '''
    def __init__(self,
                 event_pulses,
                 q_thresh,
                 delta_time_slice):
        self.event_pulses     = event_pulses
        self.q_thresh         = q_thresh
        self.delta_time_slice = delta_time_slice

        self.evid = None
        self.event = None
        self.event_hits = None
        self.tile_id = None

        self.ts = None
        self.hit_count = None

        self.time_stamps = None
        self.charges = None

        self.time_range = None

        self.event_start_time_stamp = None
        self.event_end_time_stamp   = None
    
        self.rms_of_pulse = None
        self.rms_of_wtt_region = None


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

    
    def set_ts(self,
               ts):
        ''' Sets time stamp iterator '''
        self.ts = ts


    def set_hit_count(self,
                      first_hit_at_lsb,):
        ''' Sets hit count iterator '''
        self.hit_count = 0


    def set_time_range(self,
                       time_range):
        ''' General bounds when centering plot around peak pulse '''
        self.time_range = time_range

    
    def set_event_time_stamps(self):
        ''' Sets start and end time stamps of event '''
        self.event_start_time_stamp = self.event_hits[0][3]
        self.event_end_time_stamp   = self.event_hits[-1][3]
    

    def reinitialize(self):
        ''' Reinitializes necessary class variables'''
        self.hit_count = 0
        self.ts        = 0

   
    def set_rms_of_pulse(self,
                         instile):
        ''' Sets rms value of current pulse '''
        _pulse_start_time = instile.max_peak_charge_value_time_stamps_list[0]

        _normalized_time_stamps = np.array(instile.max_peak_charge_value_time_stamps_list \
                                           - _pulse_start_time)
    
        _rms_pulse = round(np.sqrt(np.mean(_normalized_time_stamps) ** 2), 2)

        self.rms_of_pulse = _rms_pulse


    def set_rms_of_wtt_region(self,
                              time_stamps):
        ''' Sets pulse for entire region surrounding pulse '''
        _cut_time_stamps = sorted(list(time_stamps))
        _normalized_time_stamps = np.array(_cut_time_stamps - _cut_time_stamps[0])
        _rms_region = round(np.sqrt(np.mean(_normalized_time_stamps) ** 2), 2)

        self.rms_of_wtt_region = _rms_region


    def obtain_nbins(self,  
                     time_stamps):
        ''' Fetches nbins according to lsb '''
        _cut_time_stamps = sorted(list(time_stamps))
        _nbins_1_lsb = (_cut_time_stamps[-1] - _cut_time_stamps[0])
        _nbins_5_lsb = int(_nbins_1_lsb / self.delta_time_slice)
        _nbins_25_lsb = int(math.ceil(_nbins_5_lsb) / self.delta_time_slice)

        return _nbins_1_lsb, _nbins_5_lsb, _nbins_25_lsb
   

    def obtain_peak_charge_info(self,
                                instile):
        ''' Obtaining information for centering histogram on peak '''
        _peak_range_difference = instile.max_peak_charge_value_time_stamp - self.time_range
        _peak_range_addition   = instile.max_peak_charge_value_time_stamp + self.time_range

        _plot_range_start = self.event_start_time_stamp if \
                            _peak_range_difference < self.event_start_time_stamp else \
                            _peak_range_difference

        _plot_range_end = self.event_end_time_stamp if \
                          _peak_range_addition > self.event_end_time_stamp else \
                          _peak_range_addition

        return _plot_range_start, _plot_range_end


    def append_wtt_info_to_text_file(self,
                                       instile):
        ''' Appends pulse information to a text file that already exists '''
        stuff_to_write = ['',
                          'Event ' + str(self.evid),
                          'Tile ' + str(self.tile_id),
                          'rms pulse ' + str(self.rms_of_pulse),
                          'rms wtt region ' + str(self.rms_of_wtt_region),
                          'peak q ' + str(instile.max_peak_charge_value),
                          '']

        with open('wtt_information.txt', 'a') as f:
            f.writelines('\n'.join(stuff_to_write))


    def plot_charge_around_pulse(self,
                                 selection,
                                 instile):
        ''' Plots charge surrounding pulse '''
        _charges = []
        _time_stamps = []
        _range = 250
        _hit_range = 100

        self.reinitialize()

        _last_hit_index = instile.max_peak_charge_value_last_hit_index

        _iter_end = _last_hit_index + _hit_range if \
                    _last_hit_index + _hit_range < len(self.event_hits) - 1 else \
                    len(self.event_hits) - 1

        # iterate through hits and append charge/time stamps
        while self.hit_count < _iter_end:
            _tile_id = selection.get_tile_id(self.event_hits[self.hit_count])
            if _tile_id == self.tile_id:
                _time_stamps.append(self.event_hits[self.hit_count][3])
                _charges.append(self.event_hits[self.hit_count][4])
            else:
                # hit occurred at a different tile
                pass
            
            self.hit_count += 1

        self.set_rms_of_pulse(instile)
        self.set_rms_of_wtt_region(_time_stamps)

        _nbins_1_lsb, _nbins_5_lsb, _nbins_25_lsb = self.obtain_nbins(_time_stamps)
        
        self.set_time_range(_range)
        
        _range_start, _range_end = self.obtain_peak_charge_info(instile)

        #self.append_wtt_info_to_text_file(instile)

        # Plot 1: 1 LSB increment 
        fig, (axs, axs_info) = plt.subplots(1, 2)
        
        axs.hist(_time_stamps,
                 weights=_charges,
                 bins=_nbins_1_lsb,
                 histtype='step',
                 label='binned')
        
        _title = 'Event {}, Tile {}'.format(self.evid, self.tile_id)

        axs.set_title(r'{}'.format(_title))
        axs.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]', loc='left')
        axs.set_ylabel(r'charge [1000 * $10^3$ e]', loc='bottom')
        axs.set_xlim(xmin=_range_start, xmax=_range_end)
        
        axs_info_test = '''1 bin := 1 LSB increment
                           plot\_range = {}
                           rms of pulse = {}
                           rms of WTT region = {}
                           peak charge value = {}
                           peak charge value ts = {}
                        '''.format(_range_end - _range_start,
                                   self.rms_of_pulse,
                                   self.rms_of_wtt_region,
                                   instile.max_peak_charge_value,
                                   instile.max_peak_charge_value_time_stamp)

        axs_info.text(0.1, 0.60, axs_info_test, transform=axs_info.transAxes, fontsize=11, 
                      verticalalignment='top')
        axs_info.set_xticklabels([])
        axs_info.set_yticklabels([])
        axs_info.set_xticks([])
        axs_info.set_yticks([])

        # Plot 2: number of sliding window entries (5 LSB increments) 
        fig2, (ax2, ax2_info) = plt.subplots(1, 2) 
        ax2.hist(_time_stamps,
                 weights=_charges,
                 bins=_nbins_5_lsb,
                 histtype='step',
                 label='binned')
        _title_2 = 'Event {}, Tile {}'.format(self.evid, self.tile_id)

        ax2.set_title(r'{}'.format(_title_2))
        ax2.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]', loc='left')
        ax2.set_ylabel(r'charge [1000 * $10^3$ e]', loc='bottom')
        ax2.set_xlim(xmin=_range_start, xmax=_range_end)
        
        ax2_info_test = '''1 bin := 1 sliding window element (5 LSBs)
                           plot\_range = {}
                           rms of pulse = {}
                           rms of WTT region = {}
                           peak charge value = {}
                           peak charge value ts = {}
                        '''.format(_range_end - _range_start,
                                   self.rms_of_pulse,
                                   self.rms_of_wtt_region,
                                   instile.max_peak_charge_value,
                                   instile.max_peak_charge_value_time_stamp)

        ax2_info.text(0.1, 0.60, ax2_info_test, transform=ax2_info.transAxes, fontsize=11, 
                      verticalalignment='top')

        ax2_info.set_xticklabels([])
        ax2_info.set_yticklabels([])
        ax2_info.set_xticks([])
        ax2_info.set_yticks([])


        # Plot 3: 5 sliding window entries per bin (25 LSBs increments)
        fig3, (ax3, ax3_info) = plt.subplots(1, 2)
        ax3.hist(_time_stamps,
                 weights=_charges,
                 bins=_nbins_25_lsb,
                 histtype='step',
                 label='binned')

        _title_3 = 'Event {}, Tile {}'.format(self.evid, self.tile_id)

        ax3.set_title(r'{}'.format(_title_3))
        ax3.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]', loc='left')
        ax3.set_ylabel(r'charge [1000 * $10^3$ e]', loc='bottom')
        ax3.set_xlim(xmin=_range_start, xmax=_range_end)
        
        ax3_info_test = '''1 bin := 5 sliding window elements (25 LSBs)
                           plot\_range = {}
                           rms of pulse = {}
                           rms of WTT region = {}
                           peak charge value = {}
                           peak charge value ts = {}
                        '''.format(_range_end - _range_start,
                                   self.rms_of_pulse,
                                   self.rms_of_wtt_region,
                                   instile.max_peak_charge_value,
                                   instile.max_peak_charge_value_time_stamp)

        ax3_info.text(0.1, 0.60, ax3_info_test, transform=ax3_info.transAxes, fontsize=11, 
                      verticalalignment='top')

        ax3_info.set_xticklabels([])
        ax3_info.set_yticklabels([])
        ax3_info.set_xticks([])
        ax3_info.set_yticks([])

        plt.show()



    def display_wtt_events(self,
                           selection):
        ''' Driver function for displaying WTT events '''
        for evid in self.event_pulses:
            self.set_evid(evid)
            self.set_event_hits(selection)
            self.set_event_time_stamps()
            
            for tile_id in self.event_pulses[evid]:
                self.set_tile_id(tile_id)
                _instile = self.event_pulses[self.evid][self.tile_id]
                # plot charge around pulse 
                self.plot_charge_around_pulse(selection,
                                              _instile)

