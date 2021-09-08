import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['text.usetex'] = True

def driver():

    with open('wtt_information.txt', 'r') as f:
        contents = f.readlines()
    
    _datalog = 'datalog'
    _event   = 'Event'
    _tile    = 'Tile'
    _rms_pulse_1  = 'rms pulse 1'
    _rms_pulse_5  = 'rms pulse 5'
    _rms_pulse_25 = 'rms pulse 25'
    _rms_wtt_region_1  = 'rms wtt region 1'
    _rms_wtt_region_5  = 'rms wtt region 5'
    _rms_wtt_region_25 = 'rms wtt region 25'
    _peak_q_1  = 'peak q 1'
    _peak_q_5  = 'peak q 5'
    _peak_q_25 = 'peak q 25'
   
    rms_pulse_1_list     = []
    rms_pulse_5_list     = []
    rms_pulse_25_list    = []
    rms_wtt_region_1_list  = []
    rms_wtt_region_5_list  = []
    rms_wtt_region_25_list = []
    peak_q_1_list  = []
    peak_q_5_list  = []
    peak_q_25_list = []

    for line in contents:
        _value = None
        if line[:7] == _datalog:
            pass
        elif line[:5] == _event:
            pass
        elif line[:4] == _tile:
            pass

        elif line[:11] == _rms_pulse_1:
            _value = line[16:].replace('\n', '')
            _value = float(_value)
            rms_pulse_1_list.append(_value)
        elif line[:11] == _rms_pulse_5:
            _value = line[16:].replace('\n', '')
            _value = float(_value)
            rms_pulse_5_list.append(_value)
        elif line[:12] == _rms_pulse_25:
            _value = line[17:].replace('\n', '')
            _value = float(_value)
            rms_pulse_25_list.append(_value)

        elif line[:16] == _rms_wtt_region_1:
            _value = line[21:].replace('\n', '')
            _value = float(_value)
            rms_wtt_region_1_list.append(_value)
        elif line[:16] == _rms_wtt_region_5:
            _value = line[21:].replace('\n', '')
            _value = float(_value)
            rms_wtt_region_5_list.append(_value)
        elif line[:17] == _rms_wtt_region_25:
            _value = line[22:].replace('\n', '')
            _value = float(_value)
            rms_wtt_region_25_list.append(_value)

        elif line[:8] == _peak_q_1:
            _value = line[13:].replace('\n', '')
            _value = float(_value)
            peak_q_1_list.append(_value)
        elif line[:8] == _peak_q_5:
            _value = line[13:].replace('\n', '')
            _value = float(_value)
            peak_q_5_list.append(_value)
        elif line[:9] == _peak_q_25:
            _value = line[14:].replace('\n', '')
            _value = float(_value)
            peak_q_25_list.append(_value)
        else:
            pass    

    wtt_list = [1 for i in range(len(rms_pulse_1_list))]
    
    print('number of wtt events: {}'.format(len(wtt_list)))
    nbins = 5
    
    # Plot 1: Pulses by 1 LSBs
    fig, axs = plt.subplots()
    axs.hist(rms_pulse_1_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    axs.set_title('Number of WTT events vs. RMS of Pulse by 1 LSB')
    axs.set_xlabel(r'charge [1000 * $10^3$ e]')
    axs.set_ylabel(r'WTT events')

    # Plot 2: Pulses by 5 LSBs
    fig2, ax2 = plt.subplots()
    ax2.hist(rms_pulse_5_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax2.set_title('Number of WTT events vs. RMS of Pulse by 5 LSBs')
    ax2.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax2.set_ylabel(r'WTT events')
    
    # Plot 3: Pulses by 25 LSBs
    fig3, ax3 = plt.subplots()
    ax3.hist(rms_pulse_25_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax3.set_title('Number of WTT events vs. RMS of Pulse by 25 LSBs')
    ax3.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax3.set_ylabel(r'WTT events')

    # Plot 4: Peak charge by 1 LSB
    fig4, ax4 = plt.subplots()
    ax4.hist(peak_q_1_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax4.set_title('Number of WTT events vs. Peak Charge Value by 1 LSB')
    ax4.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax4.set_ylabel(r'WTT events')

    # Plot 5: Peak charge by 5 LSBs
    fig5, ax5 = plt.subplots()
    ax5.hist(peak_q_5_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax5.set_title('Number of WTT events vs. Peak Charge Value by 5 LSBs')
    ax5.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax5.set_ylabel(r'WTT events')

    # Plot 6: Peak charge by 25 LSBs
    fig6, ax6 = plt.subplots()
    ax6.hist(peak_q_25_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax6.set_title('Number of WTT events vs. Peak Charge Value by 25 LSBs')
    ax6.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax6.set_ylabel(r'WTT events')

    # Plot 7: wtt region by 1 LSBs
    fig7, ax7 = plt.subplots()
    ax7.hist(rms_wtt_region_1_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax7.set_title('number of wtt events vs. rms of wtt region by 1 LSB')
    ax7.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax7.set_ylabel(r'WTT events')

    # Plot 8: wtt region by 5 LSBs
    fig8, ax8 = plt.subplots()
    ax8.hist(rms_wtt_region_5_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax8.set_title('number of wtt events vs. rms of wtt region by 5 LSBs')
    ax8.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax8.set_ylabel(r'WTT events')
    
    # Plot 9: wtt region by 25 LSBs
    fig9, ax9 = plt.subplots()
    ax9.hist(rms_wtt_region_25_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax9.set_title('number of wtt events vs. rms of wtt region by 25 LSBs')
    ax9.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax9.set_ylabel(r'WTT events')

    plt.show()



def main():
    driver()


main()
