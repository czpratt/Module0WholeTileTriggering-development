'''
This file stores the functions used to create mp4 plots of whole tile trigger 
(WTT) events.
'''
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as ani
import imageio
import random


def rand_evt_select(num_rand_evts, num_data_events):
    #Generate an array of random event numbers
    event_arr = []
    for i in np.arange(num_rand_evts):
        rand = random.randint(0,num_data_events)
        event_arr.append(rand)
    return event_arr


def event_tile_gif(selection, tile_ids, event_ids):
    '''
    This function takes inputs from plot_tile_density and makes 
    a gif of the triggered *Tile* of the WTT event so that we 
    can better visualize the evt
    '''
    for m in event_ids:
        event_id = m
        event = selection.get_event(m)
        hits = selection.get_event_hits(event)
        tile_index = event_ids.index(m)
        tile = tile_ids[tile_index]

        px = hits['px']
        py = hits['py']
        pt = hits['ts']

        plot_px = []
        plot_py = []
        plot_pt = []

        for i in np.arange(len(px)):
            tile_id = selection.get_tile_id(hits[i])
            if tile_id == tile:
                plot_px.append(px[i])
                plot_py.append(py[i])
                plot_pt.append(pt[i])

        num_images = 100 #The number of images to compile into a gif/mp4
        section_widths = (max(plot_pt) - min(plot_pt))/num_images

        gif_px = [] #To store arrays for each of he num_images sections
        gif_py = []
        gif_pt = []

        for i in np.arange(num_images):
            max_edge = min(plot_pt) + ((i+1)*section_widths)

            temp_px = []
            temp_py = []
            temp_pt = []

            for j in np.arange(len(plot_pt)):
                if plot_pt[j] < max_edge:
                    temp_px.append(plot_px[j])
                    temp_py.append(plot_py[j])
                    temp_pt.append(plot_pt[j])

            gif_px.append(temp_px)
            gif_py.append(temp_py)
            gif_pt.append(temp_pt)

        images = []

        for k in np.arange(num_images):
            if k%5 == 0:
                print('{}/{} Gif Event Images Compiled'.format(k, num_images))
            gif_fig, gif_axes = plt.subplots()
            scat = gif_axes.scatter(np.array(gif_px[k]), 
                                    np.array(gif_py[k]), 
                                    c=np.array(gif_pt[k]), 
                                    vmin=min(plot_pt), 
                                    vmax=max(plot_pt),
                                    marker='.',
                                    s=40
                                    )
            plt.xlim(min(plot_px), max(plot_px))
            plt.ylim(min(plot_py),max(plot_py))
            gif_axes.axes.set_aspect('equal')
            gif_axes.set_xlabel('x position [mm]')
            gif_axes.set_ylabel('y position [mm]')
            gif_axes.set_title(
                'Time Histogram, Event{}, Tile{}'.format(event_id,tile)
                )
            gif_fig.colorbar(scat, 
                            ax = gif_axes, 
                            label='Detector Time', 
                            location='bottom'
                            )

            plt.savefig('gif_save.png')
            images.append(imageio.imread('gif_save.png'))
            plt.close()

        imageio.mimsave('event{}_tile{}.mp4'.format(event_id, tile), 
                        images, 
                        fps=7
                        )



def event_gif(selection, event_ids):
    '''
    This function takes inputs from plot_tile_density and makes 
    a gif of the *ENTIRE* WTT event so that we can better visualize the evt
    '''
    asic_length = 31 #The length/width of a single ASIC in mm
    tpc_length = 1240 #[mm]
    tpc_width = 620 #[mm]
    scatter_width = tpc_width/2
    scatter_length = tpc_length/2

    for m in event_ids:
        event_id = m
        event = selection.get_event(m)
        hits = selection.get_event_hits(event)

        plot_px = hits['px']
        plot_py = hits['py']
        plot_pt = hits['ts']

        num_images = 100 #The number of images to compile into gif/mp4
        section_widths = (max(plot_pt) - min(plot_pt))/num_images

        gif_px = [] #To store arrays for each of he num_images sections
        gif_py = []
        gif_pt = []

        for i in np.arange(num_images):
            max_edge = min(plot_pt) + ((i+1)*section_widths)

            temp_px = []
            temp_py = []
            temp_pt = []

            for j in np.arange(len(plot_pt)):
                if plot_pt[j] < max_edge:
                    temp_px.append(plot_px[j])
                    temp_py.append(plot_py[j])
                    temp_pt.append(plot_pt[j])

            gif_px.append(temp_px)
            gif_py.append(temp_py)
            gif_pt.append(temp_pt)

        images = []

        for k in np.arange(num_images):
            if k%5 == 0:
                print('{}/{} Gif Event Images Compiled'.format(k, num_images))
            img_time = (min(plot_pt) + ((k+0.5)*section_widths)).astype(int)
            gif_fig, gif_axes = plt.subplots(figsize=(4,8))
            scat = gif_axes.scatter(np.array(gif_px[k]),
                                    np.array(gif_py[k]),
                                    c=np.array(gif_pt[k]),
                                    vmin=min(plot_pt),
                                    vmax=max(plot_pt),
                                    marker='.',
                                    s=40
                                    )
            plt.xlim(min(plot_px), max(plot_px))
            plt.ylim(min(plot_py),max(plot_py))
            gif_axes.axes.set_aspect('equal')
            gif_axes.set_xlim(-scatter_width,scatter_width)
            gif_axes.set_ylim(-scatter_length,scatter_length)
            gif_axes.set_xlabel('x position [mm]')
            gif_axes.set_ylabel('y position [mm]')
            gif_axes.set_title('Time {}, Event{}'.format(img_time, event_id))
            gif_fig.colorbar(scat,
                            ax = gif_axes,
                            label='Detector Time',
                            location='bottom'
                            )

            for p in np.arange((tpc_width/asic_length)):
                posn = -scatter_width + asic_length*p
                if p%10==0:
                    gif_axes.axvline(x=posn,
                                    ymin=-scatter_length,
                                    ymax=scatter_length,
                                    color='r',
                                    linewidth=0.3
                                    )
                else:
                    gif_axes.axvline(x=posn,
                                    ymin=-scatter_length,
                                    ymax=scatter_length,
                                    color='b',
                                    linewidth=0.1
                                    )

            for l in np.arange((tpc_length/asic_length)):
                posn = -scatter_length + asic_length*l
                if l%10==0:
                    gif_axes.axhline(y=posn,
                                    xmin=-scatter_width,
                                    xmax=scatter_width,
                                    color='r',
                                    linewidth=0.3
                                    )
                else:
                    gif_axes.axhline(y=posn,
                                    xmin=-scatter_width,
                                    xmax=scatter_width,
                                    color='b',
                                    linewidth=0.1
                                    )

            plt.savefig('gif_save.png')
            images.append(imageio.imread('gif_save.png'))
            plt.close()

        imageio.mimsave('event{}.mp4'.format(event_id), images, fps=7)