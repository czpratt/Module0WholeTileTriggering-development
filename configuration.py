import yaml
import numpy as np

from typing import Tuple, List

class Configuration:
    '''
    Configuration class for tile layout .yaml file
    '''
    def __init__(self, 
                 tile_layout: str='',
                 num_chips_per_tile: int=1000) -> None:
       
       # load multi-tile layout yaml file
       try:
           with open(tile_layout, 'r') as _file:
               self.tile_layout = yaml.load(_file, Loader=yaml.FullLoader)
       except FileNotFoundError:
           print('Could not find geometry file ({})'.format(tile_layout))
       print('Geometry file ({}) imported successfully'.format(tile_layout))
       
       # generate configuration
       self.chips_per_tile    = num_chips_per_tile
       self.tile_positions    = np.array(
           list(self.tile_layout['tile_positions'].values()))

       self.tile_orientations = np.array(
           list(self.tile_layout['tile_orientations'].values()))

       self.io_group_io_channel_to_tile = self.get_io_group_io_channel_to_tile(
                                          self.tile_layout, \
                                          self.chips_per_tile)

    def __getitem__(self,
                    io_group_io_channel: Tuple[int, int]) -> int:
        '''
        Get a tile id for a specific (io_group,io_channel) pair,
        e.g. 
            config = Configuration(yaml_file)
            tile = config[1,1]                 # returns the tile with
                                               # io_group = 1, io_channel = 1
        
        *** returning -1 for now -- currently error with n_ext_trig causing
                                    tile layout error
        '''
        try:
            tile_id = self.io_group_io_channel_to_tile[io_group_io_channel]
        except:
            tile_id = -1
        return tile_id


    def get_io_group_io_channel_to_tile(self,
                                        yaml_file: str = '',
                                        num_chips_per_tile: int = 1000) -> dict:
        '''
        Obtains all groupings of io_group and io_channel needed in order to 
        find tile_id's - c/p'd from module0_evd.py with some modifications 
        called by: driver
        '''
        mm2cm                       = 0.1   # convert mm in yaml file to cm
        pixel_pitch                 = yaml_file['pixel_pitch'] * mm2cm
        chip_channel_to_position    = yaml_file['chip_channel_to_position']
        tile_chip_to_io             = yaml_file['tile_chip_to_io']
        io_group_io_channel_to_tile = {}
        
        for tile in tile_chip_to_io:
            for chip in tile_chip_to_io[tile]:
                io_group_io_channel  = tile_chip_to_io[tile][chip]
                io_group             = io_group_io_channel // num_chips_per_tile
                io_channel           = io_group_io_channel % num_chips_per_tile
                io_group_io_channel_to_tile[(io_group,io_channel)] = tile
        
        return io_group_io_channel_to_tile
