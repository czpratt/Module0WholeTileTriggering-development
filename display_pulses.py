'''

    Script for plotting functionality for pulse information

'''
import math
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
    _nbins       = None
    bin_width    = 10
    
    # iterate through the number of pulses stored by the instile,
    # and plot histogram
    for i in range(0, instile.npulse_count, 1):
        _time_stamps = list(instile.time_stamps_list[i])
        _charges     = list(instile.charges_list[i])
        _nbins       = math.ceil(len(_charges) / bin_width)
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


def plot_event_charge_vs_hid(selection,
                             evid):
    ''' Plotting event charge vs. hit ids '''
    _event_hits = selection.get_event_hits(selection.get_event(evid))
    
    # first lets do it for the whole event
    _charges = [] # list for obtaining charges
    _hids    = []
    
    # get list of charges for whole event
    for i in range(len(_event_hits)):
        _charges.append(_event_hits[i][4])
        _hids.append(i)

    bin_width = 10
    _nbins = math.ceil(len(_charges) / bin_width)

    fig, axs = plt.subplots()
    axs.hist(_hids,
            weights=_charges,
            bins=_nbins,
            histtype='step',
            label='binned')

    _title = 'Event {} Charge vs. Hit ID'.format(evid)
    axs.set_title(r'{}'.format(_title))
    axs.set_xlabel(r'Hit ID')
    axs.set_ylabel(r'charge [1000 * $10^3$ e]')

    plt.show()


def plot_pulse_charge_vs_hid(selection,
                             instile,
                             evid,
                             tile_id):
    ''' Plotting specific pulse charge vs hid ''' 
    _event_hits = selection.get_event_hits(selection.get_event(evid))

    _charges = []
    _hids    = []

    # iterate through all pulses on a tile
    for pulse in range(instile.npulse_count):

        _hit_start = instile.first_hit_at_lsb_index[pulse]
        _hit_end   = instile.last_hit_at_lsb_index[pulse]

        for hit_count in range(_hit_start, _hit_end + 1, 1):
            _tile_id = selection.get_tile_id(_event_hits[hit_count]) 
            
            if _tile_id == tile_id:
                _charges.append(_event_hits[hit_count][4])
                _hids.append(hit_count)
        
        bin_width = 10
        _nbins = math.ceil(len(_hids) / bin_width)

        fig, axs = plt.subplots()
        axs.hist(_hids,
                weights=_charges,
                bins=_nbins,
                histtype='step',
                label='binned')

        _title = 'Event {}, Tile {}: Charge vs. Hit ID'.format(evid,
                                                               tile_id)
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
    '''
    for evid in event_pulses:
        print('displaying pulses from event {}'.format(evid))
        
        # display entire event charge vs hid
        '''
        plot_event_charge_vs_hid(selection,
                                 evid)
        '''
        for tile_id in event_pulses[evid]:
            _instile = event_pulses[evid][tile_id]
            
            # display pulse charge vs hid plot
            '''
            plot_pulse_charge_vs_hid(selection,
                                     _instile,
                                     evid,
                                     tile_id)
            '''

            # display pulse histogram
            '''
            plot_pulse_histogram(_instile,
                                 q_thresh,
                                 delta_time_slice)
            '''
