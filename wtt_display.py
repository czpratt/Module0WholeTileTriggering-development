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

        self.evid       = None
        self.event      = None
        self.event_hits = None
        self.tile_id    = None
        self.ts         = None
        self.hit_count  = None

        self.time_stamps = None
        self.charges     = None
        self.time_range  = None

        self.event_start_time_stamp = None
        self.event_end_time_stamp   = None
    
        self.peak_charge_value_one_lsb = None 
        
        self.rms_of_pulse_one_lsb = None
        self.rms_of_pulse_5_lsb   = None
        self.rms_of_pulse_25_lsb  = None
        
        self.rms_of_wtt_region_one_lsb = None
        self.rms_of_wtt_region_5_lsb   = None
        self.rms_of_wtt_region_25_lsb  = None


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
                         selection,
                         instile):
        ''' Sets rms value of current pulse '''
        _hit_count = instile.max_peak_charge_value_first_hit_index
        _charges = []
        _time_stamps = []

        while _hit_count < instile.max_peak_charge_value_last_hit_index:
            _tile_id = selection.get_tile_id(self.event_hits[_hit_count])
            if _tile_id == self.tile_id:
                _charges.append(self.event_hits[_hit_count][4])
                _time_stamps.append(self.event_hits[_hit_count][3])
            else:
                # hit occurred at a different tile
                pass
        
            _hit_count += 1
         
        _charges_by_lsb = self.sort_charges_by_one_lsb(_charges,
                                                       _time_stamps)

        self.peak_charge_value_one_lsb = max(_charges_by_lsb)
       
        # now compute rms for every 5 lsb's (one sliding window element) 
        _charges_by_5_lsb = np.add.reduceat(_charges_by_lsb, np.arange(0, len(_charges_by_lsb), 5))
        _charges_by_25_lsb = np.add.reduceat(_charges_by_lsb, np.arange(0, len(_charges_by_lsb), 25))

        _np_charges = np.array(_charges_by_lsb)
        _np_charges_5 = np.array(_charges_by_5_lsb)
        _np_charges_25 = np.array(_charges_by_25_lsb)
        
        _rms_pulse_one = round(np.sqrt(np.mean(_np_charges) ** 2), 2)
        _rms_pulse_5 = round(np.sqrt(np.mean(_np_charges_5) ** 2), 2)
        _rms_pulse_25 = round(np.sqrt(np.mean(_np_charges_25) ** 2), 2)
        
        self.rms_of_pulse_one_lsb = _rms_pulse_one
        self.rms_of_pulse_5_lsb   = _rms_pulse_5 
        self.rms_of_pulse_25_lsb  = _rms_pulse_25


    def sort_charges_by_one_lsb(self,
                                charges,
                                time_stamps):
        ''' Sorts charges per lsb '''
        _current_lsb = None
        _charge_accumulator = 0

        _charge_by_lsb = []
        _ts_by_lsb     = []

        normalized_time_stamps = list(sorted(set(time_stamps))) 
        index = 0

        for ts in range(len(normalized_time_stamps)):
            _current_lsb = normalized_time_stamps[ts]

            while _current_lsb == time_stamps[index]:
                _charge_accumulator += charges[index]
                index += 1
                if index >= len(charges):
                    break

            # at the end, log stuff
            _charge_by_lsb.append(_charge_accumulator)
            _charge_accumulator = 0
      
        return _charge_by_lsb


    def set_rms_of_wtt_region(self,
                              selection,
                              instile,
                              time_stamps,
                              hit_indices):
        ''' Sets pulse for entire region surrounding pulse '''
        _time_range = 250  # independent of plotting (for now?)

        _ts_difference = instile.max_peak_charge_value_time_stamp - _time_range
        _ts_addition   = instile.max_peak_charge_value_time_stamp + _time_range

        _ts_start = self.event_start_time_stamp if \
                    _ts_difference < self.event_start_time_stamp else \
                    _ts_difference

        _ts_end   = self.event_end_time_stamp if \
                    _ts_addition > self.event_end_time_stamp else \
                    _ts_addition

        _hit_index_start = None
        _hit_index_end   = None
        _hit_start_flag  = False

        _hit_count = 0

        _rough_range = 50 # necessary since each LSB doesn't guarentee a hit
        _scale       = 4  # completely arbitrary for now

        _ts         = None # time incrementor
        _ts_hit_end = None # end time stamp

        _charges     = [] # intermediate charge log
        _time_stamps = [] # accompanying time stamps
    
        # temporary method of keeping track of index within rms range
        for ts in range(len(time_stamps)):
            if abs(time_stamps[ts] - _ts_start) < _rough_range and _hit_start_flag == False:
               # log starting points
               _ts = time_stamps[ts]
               _hit_index_start = hit_indices[ts]
               _hit_start_flag = True
                
            # the end hit index can be finnecky 
            elif abs(time_stamps[ts] - _ts_end) < (_rough_range * _scale) and _hit_start_flag == True:
                _hit_index_end = hit_indices[ts] 
                _ts_hit_end = time_stamps[ts]
                break
                
        _hit_count = _hit_index_start

        if _ts_hit_end == None:
            _ts_hit_end = self.event_hits[-1][3]

        if _ts == None:
            _ts = self.event_hits[0][3]

        if _hit_count == None:
            _hit_count = 0
        
        # iterate through time slice
        while _ts < _ts_hit_end:
            _tile_id = selection.get_tile_id(self.event_hits[_hit_count])
           
            print('{}, {}'.format(_hit_count, len(self.event_hits)))
            # check if there's a time match
            if _ts == self.event_hits[_hit_count][3]:

                # check if the tile id matches
                if _tile_id == self.tile_id:
                    _charges.append(self.event_hits[_hit_count][4])
                    _time_stamps.append(_ts)
                else:
                    pass
                _hit_count += 1
            
            else:
                # no hit, increment time
                _ts += 1

        
        # obtain charges by lsb
        _charges_by_lsb = self.sort_charges_by_one_lsb(_charges,
                                                       _time_stamps)

        _np_charges = np.array(_charges_by_lsb)
        _rms_region_one_lsb = round(np.sqrt(np.mean(_np_charges) ** 2), 2)
        
        # now compute rms for every 5 lsb's (one sliding window element) 
        _charges_by_5_lsb = np.add.reduceat(_charges_by_lsb, np.arange(0, len(_charges_by_lsb), 5))
        _charges_by_25_lsb = np.add.reduceat(_charges_by_lsb, np.arange(0, len(_charges_by_lsb), 25))

        _np_charges_5 = np.array(_charges_by_5_lsb)
        _np_charges_25 = np.array(_charges_by_25_lsb)
        
        _rms_wtt_region_5_lsb = round(np.sqrt(np.mean(_np_charges_5) ** 2), 2)
        _rms_wtt_region_25_lsb = round(np.sqrt(np.mean(_np_charges_25) ** 2), 2)

        self.rms_of_wtt_region_one_lsb = _rms_region_one_lsb
        self.rms_of_wtt_region_5_lsb   = _rms_wtt_region_5_lsb
        self.rms_of_wtt_region_25_lsb  = _rms_wtt_region_25_lsb


    def obtain_nbins(self,  
                     time_stamps):
        ''' Fetches nbins according to lsb '''
        _cut_time_stamps = sorted(list(time_stamps))
        _nbins_1_lsb = _cut_time_stamps[-1] - _cut_time_stamps[0]
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
                          'rms pulse 1 lsb ' + str(self.rms_of_pulse_one_lsb),
                          'rms pulse 5 lsb ' + str(self.rms_of_pulse_5_lsb),
                          'rms pulse 25 lsb ' + str(self.rms_of_pulse_25_lsb),
                          'rms wtt region 1 lsb ' + str(self.rms_of_wtt_region_one_lsb),
                          'rms wtt region 5 lsb ' + str(self.rms_of_wtt_region_5_lsb),
                          'rms wtt region 25 lsb ' + str(self.rms_of_wtt_region_25_lsb),
                          'peak q 1 lsb ' + str(self.peak_charge_value_one_lsb),
                          'peak q 5 lsb ' + str(instile.max_peak_charge_value),
                          'peak q 25 lsb ' + str(instile.sliding_window_max_charge_value),
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

        _hit_indices = []

        # iterate through hits and append charge/time stamps
        while self.hit_count < _iter_end:
            _tile_id = selection.get_tile_id(self.event_hits[self.hit_count])
            if _tile_id == self.tile_id:
                _time_stamps.append(self.event_hits[self.hit_count][3])
                _charges.append(self.event_hits[self.hit_count][4])
                _hit_indices.append(self.hit_count)
            else:
                # hit occurred at a different tile
                pass
            
            self.hit_count += 1

        # Get rms information
        self.set_rms_of_pulse(selection, instile)
        self.set_rms_of_wtt_region(selection, 
                                   instile,
                                   _time_stamps,
                                   _hit_indices)

        _nbins_1_lsb, _nbins_5_lsb, _nbins_25_lsb = self.obtain_nbins(_time_stamps)
        
        self.set_time_range(_range)
        
        _range_start, _range_end = self.obtain_peak_charge_info(instile)

        # uncomment for appending to wtt_information
        self.append_wtt_info_to_text_file(instile)

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
                                   self.rms_of_pulse_one_lsb,
                                   self.rms_of_wtt_region_one_lsb,
                                   self.peak_charge_value_one_lsb,
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
                                   self.rms_of_pulse_5_lsb,
                                   self.rms_of_wtt_region_5_lsb,
                                   round(instile.max_peak_charge_value, 2),
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
                                   self.rms_of_pulse_25_lsb,
                                   self.rms_of_wtt_region_25_lsb,
                                   round(instile.sliding_window_max_charge_value, 2),
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
