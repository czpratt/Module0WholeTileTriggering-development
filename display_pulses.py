'''

    Script for plotting functionality for pulse information
    ==> IN PROGRESS
    Notes:
        1) only utilize LSB-related plots for pulses
        -- for events, keep same (20, 50, 100) structure
'''
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from instile import Instile
from selection import Selection

matplotlib.rcParams['text.usetex'] = True


def plot_pulse_histogram(instile,
                         q_thresh,
                         delta_time_slice):
    ''' Plotting histogram of a pulse '''
    _time_stamps = None
    _charges     = None
    _nbins       = 50

    # iterate through the number of pulses stored by the instile,
    # and plot histogram
    for i in range(0, instile.npulse_count, 1):
        _time_stamps = list(instile.time_stamps_list[i])
        _charges     = list(instile.charges_list[i])
      
        _start_time = _time_stamps[0]
        _end_time = _time_stamps[-1]
        _nbins = int(_end_time - _start_time)
        _nbins = int(_nbins_ / delta_time_slice)
        
        fig, axs = plt.subplots()
        axs.hist(_time_stamps,
                 weights=_charges,
                 bins=_nbins,
                 histtype='step',
                 label='binned')

        _title = 'Event {}, Tile {}, nbins = {}, q\_thresh = {}, $\Delta$T = {}'.format(
                                                                                 instile.evid,
                                                                                 instile.tile_id,
                                                                                 _nbins,
                                                                                 q_thresh,
                                                                                 delta_time_slice)
        
        axs.set_title(r'{}'.format(_title))
        axs.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]')
        axs.set_ylabel(r'charge [1000 * $10^3$ e]')

        plt.show()


def plot_pulse_histogram_from_peak(selection,
                                   evid,
                                   tile_id,
                                   instile,
                                   q_thresh,
                                   delta_time_slice):
    ''' Plotting histogram of a pulse starting from peak value'''
    _time_stamps = None
    _charges     = None
    _rms         = None

    _range  = 100    # value of the range we want to plot (toggle)

    _plot_range_start = None
    _plot_range_end   = None

    _event_hits = selection.get_event_hits(selection.get_event(evid))
    
    _event_start_time = _event_hits[0][3]
    _event_end_time   = _event_hits[-1][3]

    # iterate through the number of pulses stored by the instile,
    # and plot histogram
    for i in range(0, instile.npulse_count, 1):
        _time_stamps = list(instile.time_stamps_list[i])
        _charges     = list(instile.charges_list[i])
       
        _start_time = _time_stamps[0]
        _end_time   = _time_stamps[-1]
      
        # normalized time stamps and compute rms
        _normalized_time_stamps = np.array(_time_stamps - _start_time)
        _rms = round(np.sqrt(np.mean(np.array(_normalized_time_stamps) ** 2)), 2)
    
        # peak charge value information (based on time slice)
        _peak_charge_value = round(instile.peak_charge_value_list[i], 2)
        _peak_charge_value_time_stamp = instile.peak_charge_value_time_stamp_list[i]
        
        # (based on collected hit information)
        _peak_charge_index     = _charges.index(max(_charges))
        _ts_at_peak_charge     = _time_stamps[_peak_charge_index]
        _peak_range_difference = _ts_at_peak_charge - _range
        _peak_range_addition   = _ts_at_peak_charge + _range

        # obtain nbins for lsb increment and # fifo entries
        _nbins_lsb        = int(_time_stamps[-1] - _time_stamps[0])
        _nbins_time_slice = int(_nbins_lsb / delta_time_slice)

        # obtain plot ranges
        _plot_range_start = _event_start_time if _peak_range_difference < _event_start_time \
                            else _peak_range_difference 
        _plot_range_end   = _event_end_time if _peak_range_addition < _event_start_time \
                            else _peak_range_addition 
        _plot_range = _plot_range_end - _plot_range_start

        # plot
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.hist(_time_stamps,
                 weights=_charges,
                 bins=_nbins_time_slice,
                 histtype='step',
                 label='binned')
        
        ax2.hist(_time_stamps,
                 weights=_charges,
                 bins=_nbins_lsb,
                 histtype='step',
                 label='binned')
        

        _title_1 = '''Event {}, Tile {}, nbins = {} 
                    plot\_range = {}, rms = {}
                    peak charge = {}, peak charge ts = {}'''.format(evid, 
                 tile_id, 
                 _nbins_time_slice,
                 _plot_range,
                 _rms,
                 _peak_charge_value,
                 _peak_charge_value_time_stamp)
        
        _title_2 = '''Event {}, Tile {}, nbins = {} 
                    plot\_range = {}, rms = {}
                    peak charge = {}, peak charge ts = {}'''.format(evid, 
                 tile_id, 
                 _nbins_lsb,
                 _plot_range,
                 _rms,
                 _peak_charge_value,
                 _peak_charge_value_time_stamp)

        ax1.set_title(r'{}'.format(_title_1))
        ax1.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]', loc='left')
        ax1.set_ylabel(r'charge [1000 * $10^3$ e]', loc='bottom')
        ax1.set_xlim(xmin=_plot_range_start, xmax=_plot_range_end)

        ax2.set_title(r'{}'.format(_title_2))
        ax2.set_xlim(xmin=_plot_range_start, xmax=_plot_range_end)
        
        plt.show()
        

def plot_event_histogram(selection,
                         evid):
    ''' Plotting event hits on a tile as a histogram '''

    _event_hits = selection.get_event_hits(selection.get_event(evid))

    _charges = []
    _time_stamps = []

    _nbins = 100
    tile_of_choice = 7

    for hit in range(len(_event_hits)):
        tile_id = selection.get_tile_id(_event_hits[hit])
        if tile_id == tile_of_choice:
            _charges.append(_event_hits[hit][4])
        else:
            _charges.append(0)
         
        _time_stamps.append(_event_hits[hit][3])

    fig, axs = plt.subplots()
    axs.hist(_time_stamps,
             weights=_charges,
             bins=_nbins,
             histtype='step',
             label='binned')
    

    _title = 'Event {}, Tile {}: Charge vs. Time, nbins = {}'.format(evid, 
                                                                       tile_of_choice,
                                                                       _nbins)
    axs.set_title(r'{}'.format(_title))
    axs.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]')
    axs.set_ylabel(r'charge [1000 * $10^3$ e]')

    plt.show()


def plot_event_charge_vs_hid(selection,
                             evid):
    ''' Plotting event charge vs. hit ids '''
    _event_hits = selection.get_event_hits(selection.get_event(evid))
    
    _charges = [] # list for obtaining charges
    _hids    = [] # list for hit id's
   
    _nbins = 50
    tile_of_choice = 7

    # get list of charges for whole event
    for i in range(len(_event_hits)):
        tile_id = selection.get_tile_id(_event_hits[i])
        if tile_id == tile_of_choice:
            _charges.append(_event_hits[i][4])
            _hids.append(i)

    fig, axs = plt.subplots()
    axs.hist(_hids,
            weights=_charges,
            bins=_nbins,
            histtype='step',
            label='binned')

    _title = 'Event {}, Tile {}: Charge vs. Hit ID, nbins = {}'.format(evid, 
                                                                       tile_of_choice,
                                                                       _nbins)
    axs.set_title(r'{}'.format(_title))
    axs.set_xlabel(r'Hit ID')
    axs.set_ylabel(r'charge [1000 * $10^3$ e]')

    plt.show()


def plot_pulse_charge_vs_hid(selection,
                             instile,
                             evid,
                             tile_id,
                             delta_time_slice):
    ''' Plotting specific pulse charge vs hid ''' 
    _event_hits = selection.get_event_hits(selection.get_event(evid))

    _charges = []
    _hids    = []

    # iterate through all pulses on a tile
    for pulse in range(instile.npulse_count):

        _hit_start = instile.first_hit_at_lsb_index[pulse]
        _hit_end   = instile.last_hit_at_lsb_index[pulse]

        _time_stamps = list(instile.time_stamps_list[pulse])
        
        _start_time = _time_stamps[0]
        _end_time = _time_stamps[-1]

        # toggle binning
        _nbins = int(_end_time - _start_time)
        #_nbins = int(_nbins_ / delta_time_slice)
        
        for hit_count in range(_hit_start, _hit_end + 1, 1):
            _tile_id = selection.get_tile_id(_event_hits[hit_count]) 
            
            if _tile_id == tile_id:
                _charges.append(_event_hits[hit_count][4])
                _hids.append(hit_count)


        fig, axs = plt.subplots()
        axs.hist(_hids,
                weights=_charges,
                bins=_nbins,
                histtype='step',
                label='binned')

        _title = 'Event {}, Tile {}: Charge vs. Hit ID, nbins = {}'.format(evid,
                                                                           tile_id,
                                                                           _nbins)
        axs.set_title(r'{}'.format(_title))
        axs.set_xlabel(r'Hit ID')
        axs.set_ylabel(r'charge [1000 * $10^3$ e]')

        plt.show()
        

def display(selection,
            event_pulses,
            q_thresh,
            delta_time_slice):
    ''' 
        Driver for displaying pulse information
        NOTES:
            1) Can turn this into a menu eventually
            2) No class implementation for now 
            ==> these are development functions
    '''
    for evid in event_pulses:
        print('displaying pulses from event {}'.format(evid))
        
        # display entire event charge vs hid
        '''
        plot_event_charge_vs_hid(selection,
                                 evid)
        '''

        # plot event histogram
        '''
        plot_event_histogram(selection,
                             evid)
        '''
        for tile_id in event_pulses[evid]:
            _instile = event_pulses[evid][tile_id]
            
            # display pulse charge vs hid plot
            '''
            plot_pulse_charge_vs_hid(selection,
                                     _instile,
                                     evid,
                                     tile_id,
                                     delta_time_slice)
            '''
            
            '''
            # display pulse histogram centered at peak value
            plot_pulse_histogram_from_peak(selection,
                                           evid,
                                           tile_id,
                                           _instile,
                                           q_thresh,
                                           delta_time_slice)
            '''
