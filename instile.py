from collections import deque

class Instile:
    ''' 
       INformation Storage about a TILE (Instile) 
       ==> stores information about a tile
        throughout an event, including its charge window, 
        and potential lists to be used for histograms         
       -- this will handle prewindows, etc., eventually       
    '''
    def __init__(self,
                 max_q_window_len: int,
                 q_thresh: float,
                 tile_id: int,
                 evid: int):
                 
        self.max_q_window_len = max_q_window_len
        self.q_thresh         = q_thresh
        self.tile_id          = tile_id
        self.evid             = evid

        self.window                = None   # charge accumulation window for each time slice
        self.sliding_charge_window = None   # sliding charge window saving sum(charges)
        self.pulse_indicator       = None   # indicator for the start of a pulse 
        
        self.pulse_start_time_stamp = None  # start times of a pulse
        self.pulse_end_time_stamp   = None  # end times of a pulse

        self.peak_charge_value_list            = None
        self.peak_charge_value_time_stamp_list = None

        self.charges      = None   # list of charges from hits
        self.time_stamps  = None   # list of time stamps of hits
        self.npulse_count = None   # counts number of pulses on the tile
        
        self.charges_list       = None  # list of all charges on a tile from a pulse
        self.time_stamps_list   = None  # list of all time stamps on a tile from a pulse

        self.first_hit_at_lsb_index = None  # index of the first hit occuring at the LSB
        self.last_hit_at_lsb_index  = None  # index of last hit occuring at LSB

        self.startup()
    
    
    def startup(self):
        ''' Initialization for redundancy '''
        self.window                = deque()
        self.sliding_charge_window = deque()
        self.charges               = deque()
        self.time_stamps           = deque()
        self.pulse_indicator       = False
        self.npulse_count          = 0

        # to potentially handle multiple pulses at one tile in the same event
        self.pulse_start_time_stamp = []
        self.pulse_end_time_stamp   = []
        self.first_hit_at_lsb_index = []
        self.last_hit_at_lsb_index  = []
        self.charges_list           = []
        self.time_stamps_list       = []

        self.peak_charge_value_list = []
        self.peak_charge_value_time_stamp_list = []


    def __repr__(self):
        ''' String representation function '''
        return ('\n\nevid = {}, tile_id = {}, npulse_count = {}, \n\
start times = {}, end times = {}, len(charges_list) = {}, len(time_stamps_list) = {}\n\
first_hit_index = {}, last_hit_index = {}\npeak_charge = {}, peak_charge_ts = {}\n'.format(
                                self.evid,
                                self.tile_id,
                                self.npulse_count,
                                self.pulse_start_time_stamp,
                                self.pulse_end_time_stamp,
                                len(self.charges_list),
                                len(self.time_stamps_list),
                                self.first_hit_at_lsb_index,
                                self.last_hit_at_lsb_index,
                                self.peak_charge_value_list,
                                self.peak_charge_value_time_stamp_list))
   

    def set_pulse_start_time_stamp(self,
                                   pulse_start_time):
        ''' Start time of the pulse '''
        self.pulse_start_time_stamp.append(pulse_start_time)
    
    
    def set_pulse_end_time_stamp(self,
                                 pulse_end_time):
        ''' Start time of the pulse '''
        self.pulse_end_time_stamp.append(pulse_end_time)
    

    def set_pulse_indicator(self,
                            decision):
        ''' Sets the pulse indicator '''
        self.pulse_indicator = decision

   
    def set_first_hit_at_lsb_index(self,
                                   first_hit_at_lsb_index):
        ''' Sets the index of the first hit at lsb '''
        self.first_hit_at_lsb_index.append(first_hit_at_lsb_index)
   

    def set_last_hit_at_lsb_index(self,
                                  last_hit_at_lsb_index):
        ''' Sets the index of the last hit at lsb '''
        self.last_hit_at_lsb_index.append(last_hit_at_lsb_index)

    
    def store_charges_in_list(self):
        ''' Store individual stacks to handle multiple hits '''
        self.charges_list.append(self.charges)
   

    def store_time_stamps_in_list(self):
        ''' Store individual stacks to handle multiple hits '''
        self.time_stamps_list.append(self.time_stamps)
   
    
    def store_peak_charge_value(self,
                                charge_value):
        ''' Store peak charge value of a pulse '''
        self.peak_charge_value_list.append(charge_value)


    def store_peak_charge_value_time_stamp(self,
                                           time_stamp):
        ''' Store peak charge value time stamp '''
        self.peak_charge_value_time_stamp_list.append(time_stamp)

    
    def increment_npulse_count(self):
        ''' Increments npulse count '''
        self.npulse_count += 1

    
    def get_npulse_count(self):
        ''' Fetches npulse_count '''
        return self.npulse_count
