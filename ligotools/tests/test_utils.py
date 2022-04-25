from ligotools import readligo as rl
from ligotools import utils as lutils

from scipy.interpolate import interp1d
import json
import numpy as np
import matplotlib.mlab as mlab

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
    