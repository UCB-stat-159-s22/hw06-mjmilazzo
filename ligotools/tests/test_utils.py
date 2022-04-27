from ligotools import readligo as rl
from ligotools import utils as lutils

import json
import h5py
import numpy as np
from scipy import signal
from scipy.signal import butter, filtfilt
from scipy.interpolate import interp1d
import matplotlib.mlab as mlab


#############################################################################################

def test_utils1():
    """ test whiten func """
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))

    eventname = 'GW150914' 
    event = events[eventname]
    fn_H1 = 'data/' + event['fn_H1']              # File name for H1 data

    fs = event['fs']
    NFFT = 4*fs

    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)

    time = time_H1
    # the time sample interval (uniformly sampled!)
    dt = time[1] - time[0]

    # We will use interpolations of the ASDs computed above for whitening:
    psd_H1 = interp1d(freqs, Pxx_H1)
    strain_H1_whiten = lutils.whiten(strain_H1,psd_H1,dt)
    
    assert isinstance(strain_H1_whiten, np.ndarray)
    assert strain_H1_whiten.shape==(131072,)
    assert np.isclose(strain_H1_whiten[0], 648.16749914)


#############################################################################################

def test_utils2():
    """ test write_wavfile func """
    
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))
    
    eventname = 'GW150914'
    event = events[eventname]
    
    tevent = event['tevent']            # Set approximate event GPS time
    fband = event['fband']              # frequency band for bandpassing signal
    fn_H1 = 'data/' + event['fn_H1']    # File name for H1 data
    fs = 4096
    NFFT = 4*fs

    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')

    time = time_H1
    dt = time[1] - time[0]
    
    deltat_sound = 2.                     # seconds around the event
    indxd = np.where((time >= tevent-deltat_sound) & (time < tevent+deltat_sound))
    
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
    psd_H1 = interp1d(freqs, Pxx_H1)
    strain_H1_whiten = lutils.whiten(strain_H1,psd_H1,dt)

    bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
    normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
    strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization
    
    d = lutils.write_wavfile(
        'audio/'+eventname+"_H1_whitenbp.wav",
        int(fs), 
        strain_H1_whitenbp[indxd], 
        writeout=False,
    )
    
    assert isinstance(d, np.ndarray)
    assert d.shape[0] == 16384
    assert d[1] == 1302


#############################################################################################

def test_utils3():
    """ test reqshift func """
    
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))
    
    eventname = 'GW150914'
    event = events[eventname]
    
    fband = event['fband']              # frequency band for bandpassing signal
    fn_H1 = 'data/' + event['fn_H1']    # File name for H1 data
    fs = 4096
    NFFT = 4*fs
    fshift = 400.

    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')

    time = time_H1
    dt = time[1] - time[0]
    
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
    psd_H1 = interp1d(freqs, Pxx_H1)
    strain_H1_whiten = lutils.whiten(strain_H1,psd_H1,dt)

    bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
    normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
    strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization
    
    strain_H1_shifted = lutils.reqshift(
        strain_H1_whitenbp,
        fshift=fshift,
        sample_rate=fs
    )
    
    assert isinstance(strain_H1_shifted, np.ndarray)
    assert strain_H1_shifted.shape[0] == 131072
    assert np.isclose(strain_H1_shifted[-1], 849.52085397)


#############################################################################################

def test_utils4():
    """ test plot_PSD func """
    
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))
    
    eventname = 'GW150914'
    event = events[eventname]
    
    tevent = event['tevent']            # Set approximate event GPS time
    fband = event['fband']              # frequency band for bandpassing signal
    fn_template = 'data/' + event['fn_template']  # File name for template waveform
    fn_H1 = 'data/' + event['fn_H1']    # File name for H1 data
    fs = 4096
    NFFT = 4*fs
    fshift = 400.

    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')

    time = time_H1
    dt = time[1] - time[0]
    
    deltat_sound = 2.                     # seconds around the event
    indxd = np.where((time >= tevent-deltat_sound) & (time < tevent+deltat_sound))
    
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
    psd_H1 = interp1d(freqs, Pxx_H1)
    strain_H1_whiten = lutils.whiten(strain_H1,psd_H1,dt)

    bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
    normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
    strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization

    
    NOVL = NFFT/2
    psd_window = np.blackman(NFFT)
    
    f_template = h5py.File(fn_template, "r")
    template_p, template_c = f_template["template"][...]
    f_template.close()

    template = (template_p + template_c*1.j) 
    # the length and sampling rate of the template MUST match that of the data.
    datafreq = np.fft.fftfreq(template.size)*fs
    df = np.abs(datafreq[1] - datafreq[0])

    try:   dwindow = signal.tukey(template.size, alpha=1./8)  # Tukey window preferred, but requires recent scipy version 
    except: dwindow = signal.blackman(template.size)          # Blackman window OK if Tukey is not available

    template_fft = np.fft.fft(template*dwindow) / fs

    
    d_eff, phase, offset, template_rolled = lutils.plot_PSD(
        det='H1',
        strain_L1=None,
        strain_H1=strain_H1,
        fs=fs,
        NFFT=NFFT,
        psd_window=psd_window,
        NOVL=NOVL,
        dwindow=dwindow,
        datafreq=datafreq,
        template_fft=template_fft,
        df=df,
        time=time,
        template=template,
        dt=dt,
        bb=bb,
        ab=ab,
        normalization=normalization,
        strain_H1_whitenbp=strain_H1_whitenbp,
        strain_L1_whitenbp=None,
        eventname=eventname,
        plottype="png",
        tevent=tevent,
        make_plots=False,
    )
    
    assert np.isclose(d_eff, 814.440186711029)
    assert np.isclose(phase, 2.2419856764430532)
    assert offset==1800
    assert template_rolled.shape[0]==131072
    assert np.isclose(sum(template_rolled), 0)
