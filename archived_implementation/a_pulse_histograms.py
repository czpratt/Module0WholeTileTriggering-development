'''
    Histogram plotting functionality for pulses
'''
import numpy as np
import matplotlib.pyplot as plt

class PulseHistogram():
    def __init__(self,
                 selection,
                 evid,
                 pulses,
                 pulse_tile_id,
                 decision):
        ''' Class for a pulse histogram '''
        self.evid   = evid
        self.pulses = pulses
        self.pulse_tile_id = pulse_tile_id
        self.decision      = decision

        self.pulse_event      = None
        self.pulse_event_hits = None
        self.event_start_time = None
        self.ts               = None

        self.start_times = None
        self.end_times   = None
       
        self.min_start_time   = None
        self.max_end_time     = None
        self.pulse_time_range = None
        self.ts               = None
    
        self.hit_count = None

        self.charges      = None
        self.time_stamps  = None
        self.pulse_ids    = None
        self.end_pulse_id = None

        self.NO_HIT = -10
        self.NO_Q   = 0
        

        self.startup(selection)
    

    def assemble_charge_and_time_lists(self,
                                       selection):
        ''' Assembles list of charge and time for pulse finding '''
        while self.ts < self.max_end_time:

            # check if there's a timestep here and evaluate
            if self.ts == self.pulse_event_hits[self.hit_count][3]:

                _tile_id = selection.get_tile_id(self.pulse_event_hits[self.hit_count])

                if _tile_id == self.pulse_tile_id:
                    # a match
                    self.time_stamps.append(self.ts)
                    self.charges.append(abs(self.pulse_event_hits[self.hit_count][4])) 
                else:
                    pass

                # move onto next hit regardless
                self.hit_count += 1

            else:
                self.time_stamps.append(self.ts)
                self.charges.append(self.NO_Q)

                self.ts += self.time_step


    def plot_histogram(self):
        ''' 
            Makes histograms
            --> will probably need to adjust bin size!
        ''' 
        nbins = 300
        fig, axs = plt.subplots()
        
        # 2D color norms are weird
        axs.hist(self.time_stamps,
                 weights=self.charges,
                 bins=nbins,
                 histtype='step', 
                 label='binned')
        
        axs.set_title('Tile {}, Event {}, nbins = {}'.format(self.pulse_tile_id, 
                                                             self.evid,
                                                             nbins))
        axs.set_xlabel(r'timestep [0.1 $\mathrm{\mu}$s]')
        axs.set_ylabel(r'charge [1000 * $10^3$ e]')

        plt.show()


    def startup(self,
                selection):
        ''' Activated on creation '''
        self.pulse_event      = selection.get_event(self.evid)
        self.pulse_event_hits = selection.get_event_hits(self.pulse_event)

        pulse_event_hit_ids = []

        self.start_times = []
        self.end_times   = []
        self.pulse_ids   = []

        self.charges     = []
        self.time_stamps = []
        
        self.time_step = 1

        # inefficient but necessary for now
        # accumulate all hit id's to find a match
        for hit in self.pulse_event_hits:
            pulse_event_hit_ids.append(hit[0])

        # accumulate 'pulse' start and end times
        for pulse in self.pulses:
            self.start_times.append(pulse.pulse_start_time)
            self.end_times.append(pulse.pulse_end_time)
            self.pulse_ids.append(pulse.hit_at_start_time)

        self.min_start_time = int(min(self.start_times))
        self.max_end_time   = int(max(self.end_times))
       
        pulse_start_id       = int(min(self.pulse_ids))
        pulse_start_id_index = pulse_event_hit_ids.index(pulse_start_id)
        self.hit_count       = pulse_start_id_index
        self.ts              = self.min_start_time

        self.assemble_charge_and_time_lists(selection)
        
        if self.decision:
            self.plot_histogram()


def make_pulse_histograms(selection,
                          all_pulses,
                          decision):
    ''' Iterates through all event pulses to potentially plot histograms ''' 
    for evid in all_pulses:
        for tile_pulse in all_pulses[evid]:
            pulse_histogram = PulseHistogram(selection,
                                             evid,
                                             all_pulses[evid][tile_pulse],
                                             tile_pulse,
                                             decision)

            #del pulse_histogram

