import time
import yaml
import h5py as h

from configuration import Configuration

class Selection:
    '''
    Selection class for obtaining information about a datalog file
    '''
    def __init__(self, 
            data_file: str, 
            config_file: str,
            nhits_cut: int):

        data_load_start = time.time()

        try:
            self.data_file = h.File(data_file, 'r')
        except FileNotFoundError:
            print('Data file ({}) could not be imported.'.format(data_file))
        
        print('Data file ({}) imported successfully'.format(data_file))
        self.config              = Configuration(config_file)    
        self.ticks_per_qsum      = 10              # clock ticks per time bin
        self.t0_charge_threshold = 200.0           # Rough qsum threshold
        self.events              = self.data_file['events']  
        self.hits                = self.data_file['hits']        
        self.nhits               = self.events['nhit']           
        self.info                = self.data_file['info'].attrs # extraneous information 
        self.vdrift              = self.info['vdrift'] 
        self.clock_period        = self.info['clock_period']    
        self.ext_trigs           = self.data_file['ext_trigs'] if 'ext_trigs' \
                                   in self.data_file.keys() else None 
        self.nhits_cut       = nhits_cut
        self.nhit_cut_events = None
        data_load_end = time.time()
        print('Loaded data file {} in {} seconds'.format(data_file, data_load_end - data_load_start))

        # if nhits is non-empty, make cuts on ntiles
        if self.nhits_cut:
            nhit_cut_start = time.time()
            print('o----------------------------------------o')
            print('Starting nhit cut on events with threshold: {}'.format(self.nhits_cut))
            self.nhit_cut_events = {}
            self.make_nhit_cuts() 
            nhit_cut_end = time.time()
            print('Finished nhits cut on events in {}'.format(nhit_cut_end - nhit_cut_start))
        else:
            pass

    def __repr__(self):
        return ('nhit cut events: {}'.format(self.nhit_cut_events))


    def make_event_nhit_cut(self, 
                            evid: int):
        '''
            Makes cuts based on nhits for individual events
        '''
        if evid % 1000 == 0:
            print('Analyzing event {} of {} total events'.format(evid, self.events[-1][0]))

        _event               = self.events[evid]
        _event_hits          = self.hits[_event['hit_ref']]
        _event_hits_per_tile = {i: 0 for i in range(1, 16 + 1, 1)} # tile dictionary
        _cut_event           = None
        
        # iterate through all hits in an event
        for hit in range(len(_event_hits)):
            _tile_id    = self.get_tile_id(_event_hits[hit])
            if _tile_id == -1:
                continue
            _event_hits_per_tile[_tile_id] += 1 
            

        # at end of accumulation, check to see if any tiles pass the threshold
        _cut_event = {tile_id: nhits for (tile_id, nhits) in _event_hits_per_tile.items() 
                      if nhits > self.nhits_cut}
        
        if _cut_event:
            print('o----------------------------------------o')
            print('event {} cut events: {}'.format(evid, _cut_event))
            print('o----------------------------------------o')
            self.nhit_cut_events[evid] = _cut_event
        else:
            # no tiles past threshold, 
            # move onto next event
            pass


    def make_nhit_cuts(self):
        '''
            Driver function making cuts on all events in a datalog file
        '''
        
        #iter_start = 1
        #iter_end = len(self.events) # toggle when necessary
        #iter_end = 20000
        iter_start = 57128
        iter_end = 57132
        for event in range(iter_start, iter_end, 1):
            self.make_event_nhit_cut(event)

        return self.nhit_cut_events

    def get_tile_id(self, 
                    hit) -> int:
        ''' Fetches tile_id within selection class '''
        _io_group   = hit['iogroup']
        _io_channel = hit['iochannel']
        _tile_id = self.config[_io_group, _io_channel]
        
        return _tile_id

    def get_event(self, 
                  evid):
        ''' Fetches specific event '''
        return self.events[evid]

    def get_event_hits(self, 
                       event):
        ''' Fetches the hits within an event '''
        return self.hits[event['hit_ref']] # good

    def get_z_anode(self, 
                    tile_id):
        ''' Fetches z_anode location '''
        return self.config.tile_positions[tile_id - 1][0]
    
    def get_num_events(self):
        ''' Fetches total number of events '''
        return self.events[-1][0]

    def get_cut_events(self):
        ''' Fetches nhit cut events'''
        return self.nhit_cut_events
