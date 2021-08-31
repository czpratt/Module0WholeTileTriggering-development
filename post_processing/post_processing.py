import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['text.usetex'] = True

def driver():

    with open('wtt_information.txt', 'r') as f:
        contents = f.readlines()
    
    _datalog = 'datalog'
    _event = 'Event'
    _tile = 'Tile'
    _rms_pulse = 'rms pulse'
    _rms_wtt_region = 'rms wtt region'
    _peak_q = 'peak q'
   
    rms_pulse_list    = []
    rms_wtt_region_list = []
    peak_q_list = []

    for line in contents:
        _value = None
        if line[:7] == _datalog:
            pass
        elif line[:5] == _event:
            pass
        elif line[:4] == _tile:
            pass
        elif line[:9] == _rms_pulse:
            _value = line[10:].replace('\n', '')
            _value = float(_value)
            rms_pulse_list.append(_value)
        elif line[:14] == _rms_wtt_region:
            _value = line[15:].replace('\n', '')
            _value = float(_value)
            rms_wtt_region_list.append(_value)
        elif line[:6] == _peak_q:
            _value = line[7:].replace('\n', '')
            _value = float(_value)
            peak_q_list.append(_value)
        else:
            pass    

    wtt_list = [1 for i in range(1, len(rms_pulse_list) + 1, 1)]
    
    print('number of wtt events: {}'.format(len(wtt_list)))
    nbins = 10

    fig, axs = plt.subplots()

    axs.hist(rms_pulse_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    axs.set_title('Number of WTT events vs. RMS of Pulse')
    axs.set_xlabel(r'time [0.1 $\mu$s]')
    axs.set_ylabel(r'WTT events')

    fig2, ax2 = plt.subplots()

    ax2.hist(peak_q_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax2.set_title('Number of WTT events vs. Peak Charge Value')
    ax2.set_xlabel(r'charge [1000 * $10^3$ e]')
    ax2.set_ylabel(r'WTT events')

    fig3, ax3 = plt.subplots()

    ax3.hist(rms_wtt_region_list,
             weights=wtt_list,
             bins=nbins,
             histtype='step',
             label='binned')

    ax3.set_title('Number of WTT events vs. RMS of WTT Region')
    ax3.set_xlabel(r'time [0.1 $\mu$s]')
    ax3.set_ylabel(r'WTT events')

    plt.show()



def main():
    driver()


main()
