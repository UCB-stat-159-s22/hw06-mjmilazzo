from ligotools import readligo as rl
# from ligotools import utils as lutils

import json
# import h5py
import numpy as np
# from scipy import signal
# from scipy.signal import butter, filtfilt
# from scipy.interpolate import interp1d
# import matplotlib.mlab as mlab


#############################################################################################

def test_rl1():
    """ test 1 for loaddata func (H1)"""
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))

    eventname = 'GW150914' 
    event = events[eventname]
    fn_H1 = 'data/' + event['fn_H1']              # File name for H1 data
    
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
    
    assert isinstance(strain_H1, np.ndarray)
    assert strain_H1.shape==(131072,)
    assert np.isclose(strain_H1[0], 0)

    assert isinstance(time_H1, np.ndarray)
    assert time_H1.shape==(131072,)
    assert np.isclose(time_H1[0], 1126259446)

    assert isinstance(chan_dict_H1, dict)
    assert len(chan_dict_H1)==13


#############################################################################################

def test_rl2():
    """ test 2 for loaddata func (L1)"""
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))

    eventname = 'GW150914' 
    event = events[eventname]
    fn_L1 = 'data/' + event['fn_L1']              # File name for L1 data
    
    strain_L1, time_L1, chan_dict_L1 = rl.loaddata(fn_L1, 'L1')
    
    assert isinstance(strain_L1, np.ndarray)
    assert strain_L1.shape==(131072,)
    assert np.isclose(strain_L1[0], 0)

    assert isinstance(time_L1, np.ndarray)
    assert time_L1.shape==(131072,)
    assert np.isclose(time_L1[0], 1126259446)

    assert isinstance(chan_dict_L1, dict)
    assert len(chan_dict_L1)==13


#############################################################################################

def test_rl3():
    """ test 3 fpr dq_channel_to_seglist func (CBC_CAT3)"""
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))
    
    eventname = 'GW150914' 
    event = events[eventname]
    fn_H1 = 'data/' + event['fn_H1']              # File name for H1 data
    fn_L1 = 'data/' + event['fn_L1']              # File name for L1 data
    
    strain, time, chan_dict = rl.loaddata(fn_L1, 'H1')
    
    DQflag = 'CBC_CAT3'
    # readligo.py method for computing segments (start and stop times with continuous valid data):
    segment_list = rl.dq_channel_to_seglist(chan_dict[DQflag])
    
    assert isinstance(segment_list, list)
    assert isinstance(segment_list[0], slice)
    assert segment_list[0].start==0


#############################################################################################

def test_rl4():
    """ test 4 fpr dq_channel_to_seglist func (NO_CBC_HW_INJ)"""
    fnjson = "data/BBH_events_v3.json"
    events = json.load(open(fnjson,"r"))
    
    eventname = 'GW150914' 
    event = events[eventname]
    fn_H1 = 'data/' + event['fn_H1']              # File name for H1 data
    fn_L1 = 'data/' + event['fn_L1']              # File name for L1 data
    
    strain, time, chan_dict = rl.loaddata(fn_L1, 'H1')
    
    DQflag = 'NO_CBC_HW_INJ'
    # readligo.py method for computing segments (start and stop times with continuous valid data):
    segment_list = rl.dq_channel_to_seglist(chan_dict[DQflag])
    
    assert isinstance(segment_list, list)
    assert isinstance(segment_list[0], slice)
    assert segment_list[0].start==0
