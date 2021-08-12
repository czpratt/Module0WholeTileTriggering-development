'''
    Plotting functions
'''

def plot_py_px(_hits_dictionary, evid, _filename):
    '''
    Plotting hits occuring on each tile from 1 <= tile_ids <= 16 per event
    --> only for plotting py vs. px
    called by: driver
    '''
    # for all coordinates
    x_1 = []
    y_1 = []
    x_2 = []
    y_2 = []
    x_3 = []
    y_3 = []
    x_4 = []
    y_4 = []
    x_5 = []
    y_5 = []
    x_6 = []
    y_6 = []
    x_7 = []
    y_7 = []
    x_8 = []
    y_8 = []
    x_9 = []
    y_9 = []
    x_10 = []
    y_10 = []
    x_11 = []
    y_11 = []
    x_12 = []
    y_12 = []
    x_13 = []
    y_13 = []
    x_14 = []
    y_14 = []
    x_15 = []
    y_15 = []
    x_16 = []
    y_16 = []

    # iterate through hits in the dictionary by tile_id and organize
    for hit in _hits_dictionary.values():
        if hit[0] == 1:
            x_1.append(hit[3])
            y_1.append(hit[4])
        elif hit[0] == 2:
            x_2.append(hit[3])
            y_2.append(hit[4])
        elif hit[0] == 3:
            x_3.append(hit[3])
            y_3.append(hit[4])
        elif hit[0] == 4:
            x_4.append(hit[3])
            y_4.append(hit[4])
        elif hit[0] == 5:
            x_5.append(hit[3])
            y_5.append(hit[4])
        elif hit[0] == 6:
            x_6.append(hit[3])
            y_6.append(hit[4])
        elif hit[0] == 7:
            x_7.append(hit[3])
            y_7.append(hit[4])
        elif hit[0] == 8:
            x_8.append(hit[3])
            y_8.append(hit[4])
        elif hit[0] == 9:
            x_9.append(hit[3])
            y_9.append(hit[4])
        elif hit[0] == 10:
            x_10.append(hit[3])
            y_10.append(hit[4])
        elif hit[0] == 11:
            x_11.append(hit[3])
            y_11.append(hit[4])
        elif hit[0] == 12:
            x_12.append(hit[3])
            y_12.append(hit[4])
        elif hit[0] == 13:
            x_13.append(hit[3])
            y_13.append(hit[4])
        elif hit[0] == 14:
            x_14.append(hit[3])
            y_14.append(hit[4])
        elif hit[0] == 15:
            x_15.append(hit[3])
            y_15.append(hit[4])
        elif hit[0] == 16:
            x_16.append(hit[3])
            y_16.append(hit[4])
        else:
            print('unlogged data')


    # 4x4 subplots of tiles
    fig, axs = plt.subplots(4, 4)
    fig.suptitle(r'Event {}: py vs. px'.format(evid))

    '''    Layout:  (by tile)
           Event {}: y vs. x
     --------------------------------
     |   1       2       9       10 |
     |   3       4       11      12 |
     |   5       6       13      14 |
     |   7       8       15      16 |
     --------------------------------
    '''

    # plotting specifications
    marker_size = 0.3       # marker size
    ntile_size = 'small'    # size of "tile {}" subtitle

    # first row
    axs[0, 0].scatter(x_1, y_1, s=marker_size)          # tile 1 
    axs[0, 0].set_title('tile 1', fontsize=ntile_size)
    axs[0, 0].set_xlim(-300, 0)
    axs[0, 0].set_ylim(650, 300)
    axs[0, 1].scatter(x_2, y_2, s=marker_size)          # tile 2
    axs[0, 1].set_title('tile 2', fontsize=ntile_size)  
    axs[0, 1].set_xlim(0, 300)
    axs[0, 1].set_ylim(650, 300)
    axs[0, 2].scatter(x_9, y_9, s=marker_size)          # tile 9
    axs[0, 2].set_title('tile 9', fontsize=ntile_size)  
    axs[0, 2].set_xlim(-300, 0)
    axs[0, 2].set_ylim(650, 300)
    axs[0, 3].scatter(x_10, y_10, s=marker_size)        # tile 10
    axs[0, 3].set_title('tile 10', fontsize=ntile_size)
    axs[0, 3].set_xlim(0, 300)
    axs[0, 3].set_ylim(650, 300)
   
    # second row
    axs[1, 0].scatter(x_3, y_3, s=marker_size)          # tile 3
    axs[1, 0].set_title('tile 3', fontsize=ntile_size)  
    axs[1, 0].set_xlim(-300, 0)
    axs[1, 0].set_ylim(0, 300)
    axs[1, 1].scatter(x_4, y_4, s=marker_size)          # tile 4
    axs[1, 1].set_title('tile 4', fontsize=ntile_size)
    axs[1, 1].set_xlim(0, 300)
    axs[1, 1].set_ylim(0, 300)
    axs[1, 2].scatter(x_11, y_11, s=marker_size)        # tile 11
    axs[1, 2].set_title('tile 11', fontsize=ntile_size)
    axs[1, 2].set_xlim(-300, 0)
    axs[1, 2].set_ylim(0, 300)
    axs[1, 3].scatter(x_12, y_12, s=marker_size)        # tile 12
    axs[1, 3].set_title('tile 12', fontsize=ntile_size)
    axs[1, 3].set_xlim(0, 300)
    axs[1, 3].set_ylim(0, 300)
   
    # third row
    axs[2, 0].scatter(x_5, y_5, s=marker_size)          # tile 5
    axs[2, 0].set_title('tile 5', fontsize=ntile_size)
    axs[2, 0].set_xlim(-300, 0)
    axs[2, 0].set_ylim(-350, 0)
    axs[2, 1].scatter(x_6, y_6, s=marker_size)          # tile 6
    axs[2, 1].set_title('tile 6', fontsize=ntile_size)
    axs[2, 1].set_xlim(0, 300)
    axs[2, 1].set_ylim(-350, 0)
    axs[2, 2].scatter(x_13, y_13, s=marker_size)        # tile 13
    axs[2, 2].set_title('tile 13', fontsize=ntile_size)
    axs[2, 2].set_xlim(-300, 0)
    axs[2, 2].set_ylim(-350, 0)
    axs[2, 3].scatter(x_14, y_14, s=marker_size)        # tile 14
    axs[2, 3].set_title('tile 14', fontsize=ntile_size)
    axs[2, 3].set_xlim(0, 300)
    axs[2, 3].set_ylim(-350, 0)

    # fourth row
    axs[3, 0].scatter(x_7, y_7, s=marker_size)          # tile 7
    axs[3, 0].set_title('tile 7', fontsize=ntile_size)
    axs[3, 0].set_xlim(-300, 0)
    axs[3, 0].set_ylim(-650, -300)
    axs[3, 0].set_xlabel('px', fontsize=ntile_size)
    axs[3, 0].set_ylabel('py', fontsize=ntile_size)
    axs[3, 1].scatter(x_8, y_8, s=marker_size)          # tile 8
    axs[3, 1].set_title('tile 8', fontsize=ntile_size)
    axs[3, 1].set_xlim(0, 300)
    axs[3, 1].set_ylim(-650, -300)
    axs[3, 2].scatter(x_15, y_15, s=marker_size)        # tile 15
    axs[3, 2].set_title('tile 15', fontsize=ntile_size)
    axs[3, 2].set_xlim(-300, 0)
    axs[3, 2].set_ylim(-650, -300)
    axs[3, 3].scatter(x_16, y_16, s=marker_size)        # tile 16
    axs[3, 3].set_title('tile 16', fontsize=ntile_size)
    axs[3, 3].set_xlim(0, 300)
    axs[3, 3].set_ylim(-650, -300)

    # make string out of filename
    # ** eventually save figure if requested (just take screenshot for now)**
    #storage_place = '/' + _filename[:-3] + '/' + 'event{}'.format(evid)

    fig.tight_layout()
    plt.show()

'''
    Finds necessary hit information for all hits in a candidate event
    --> used for plotting
    called by: driver
'''
def obtain_hits_dictionary(f_info, evid, events, hits, tile_positions, tile_orientations, io_group_io_channel_to_tile):
    event         = events[evid]            # individual event
    hit_ref       = event['hit_ref']        # specifies hits associated with event
    specific_hits = hits[hit_ref]           # hits specific to an event
    unassoc_hits  = get_unassoc_hits(event, specific_hits)      # list of unassoc hits
    print('storing hits of event {}'.format(evid))
    
    event_start_time  = obtain_event_start_time(event, hits)    # timestamp of event beginning
    hits_dictionary    = {}                                     # will contain information about a hit
    
    # Iterate through an event's hits and accumulate information to return to event_dictionary 
    for j in range(len(specific_hits)):
        _io_group     = specific_hits[j][6]
        _io_channel   = specific_hits[j][5]
        _tile_id      = get_tile_id(io_group_io_channel_to_tile, _io_group, _io_channel)
        _timestamp    = unassoc_hits[j][3] - event_start_time
        _z_coordinate = obtain_z_coordinate(_tile_id, tile_positions, tile_orientations, f_info, _timestamp)
        _q            = specific_hits[j][4]
        _px           = specific_hits[j][1]
        _py           = specific_hits[j][2]

        # each hit has its own dictionary, containing:
        # -- [tile id, q, timestamp, px, py, z]
        hits_dictionary[specific_hits[j][0]] = (_tile_id, _q, _timestamp, _px, _py, _z_coordinate)
        '''
            Store all hits from an event in the dictionary as : 
            {hid_1:(tile_id_1, q_1, time_1, px_1, py_1, pz_1),
             hid_2:(tile_id_2, q_2, time_2, px_2, py_2, pz_2), 
             ...
            }
        '''

    print('event {} information stored'.format(evid))
    return hits_dictionary


def plot_tile_density(event,tile,hits):
    '''
    In order to create a 2d histogram of the x-view and y-view 
    (in terms of tiles) in which the density is the time the hit was recorded
    '''
    #print(hits)
    px = hits['px']
    plot_px = []
    py = hits['py']
    plot_py = []
    pt = hits['ts']
    plot_pt = []
    iterator = np.arange(len(px))

    for l in iterator:
        _io_group     = hits[l][6]
        _io_channel   = hits[l][5]
        _tile_id      = selection.config[_io_group, _io_channel]
        if _tile_id == tile:
            plot_px.append(px[l])
            plot_py.append(py[l])
            plot_pt.append(pt[l])

    #figure, h = plt.subplots(2,1)
    plt.figure()
    h1 = plt.hist2d(plot_px, plot_py, bins=100, weights=plot_pt)
    plt.colorbar(label='Detector Time')
    plt.xlabel('x position')
    plt.ylabel('y position')
    plt.title('Time Histo, Event:{} Tile:{}'.format(event,tile))
    plt.show()

    #Now, let's average the times that we plot and make a "residuals" plot
    average = sum(plot_pt)/len(plot_pt)
    diff_pt = plot_pt - average

    plt.figure()
    h2 = plt.hist2d(plot_px, plot_py, bins=100, weights=diff_pt)
    plt.colorbar(label='Detector Time Difference')
    plt.xlabel('x position')
    plt.ylabel('y position')
    plt.title('Time Residuals Histo, Event:{} Tile:{}'.format(event,tile))
    plt.show()

    #Perhaps the large range of times might be eclipsing our view. 
    # Let's place cuts
    diff_min = -1000
    diff_max = 1000

    plt.figure()
    h3 = plt.hist2d(
        plot_px, 
        plot_py, 
        bins=100, 
        weights=diff_pt, 
        cmax=diff_max, 
        cmin=diff_min
    )
    plt.colorbar(label='Detector Time Difference')
    plt.xlabel('x position')
    plt.ylabel('y position')
    plt.title('Time Residuals Histo, Event:{} Tile:{}'.format(event,tile))
    plt.show()
