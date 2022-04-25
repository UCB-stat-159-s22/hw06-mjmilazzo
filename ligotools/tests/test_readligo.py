from ligotools import readligo as rl
import numpy as np
import json

def test_rl1():
    """ test data loading func """
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))

    eventname = 'GW150914' 
    event = events[eventname]
    fn_H1 = 'data/' + event['fn_H1']              # File name for H1 data

    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')

    assert isinstance(strain_H1, np.ndarray)
    assert strain_H1.shape==(131072,)
    assert np.isclose(strain_H1[0], 2.17704028e-19)