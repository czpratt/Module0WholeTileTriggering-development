'''

    Script for plotting informationa about pulses

'''
import matplotlib.pyplot as plt
import matplotlib
import math
from instile import Instile

matplotlib.rcParams['text.usetex'] = True


def plot_pulse_histogram(instile,
                         q_thresh,
                         delta_time_slice):
    ''' Plotting histogram of a pulse '''
    _time_stamps = None
    _charges     = None
    _nbins       = None
    bin_width    = 10
    
    # iterate through the number of pulses stored by the instile
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


def display(event_pulses,
            q_thresh,
            delta_time_slice):
    ''' 
        Driver for displaying pulse information
        NOTES:
            1) Can turn this into a menu eventually
            2) No class necessary, just need to pass event_pulses
               around
            3) event_pulses[evid][tile_id] := instile containing pulse information
    '''
    for evid in event_pulses:
        for tile_id in event_pulses[evid]:
            plot_pulse_histogram(event_pulses[evid][tile_id],
                                 q_thresh,
                                 delta_time_slice)
