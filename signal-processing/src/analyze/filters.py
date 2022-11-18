import peakutils #peak detection
import numpy as np #to handle datas
import math #to handle mathematical stuff (example power of 2)
import scipy
from scipy.signal import butter, lfilter, welch, square  #for signal filtering

###############################################################################
#                                                                             #
#                              FILTERS                                        #
#                                                                             #
###############################################################################
    
#Define the filters
def butter_lowpass(cutoff, fs, order=5):
    """ This functions generates a lowpass butter filter
    
        :param cutoff: cutoff frequency
        :type cutoff: float
        :param cutoff: cutoff frequency
        :type cutoff: float
        :param fs: samplerate of the signal
        :type fs: float
        :param order: order of the Butter Filter
        :type order: int
        :return: butter lowpass filter
        :rtype: list
    """
    nyq = 0.5 * fs #Nyquist frequeny is half the sampling frequency
    normal_cutoff = cutoff / nyq 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return(b, a)
    
def butter_highpass(cutoff, fs, order=5):
    """ This functions generates a higpass butter filter
    
        :param cutoff: cutoff frequency
        :type cutoff: float
        :param cutoff: cutoff frequency
        :type cutoff: float
        :param fs: samplerate of the signal
        :type fs: float
        :param order: order of the Butter Filter
        :type order: int
        :return: butter highpass filter
        :rtype: list
    """
    nyq = 0.5 * fs #Nyquist frequeny is half the sampling frequency
    normal_cutoff = cutoff / nyq 
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return(b, a)
    
def butter_lowpass_filter(data, cutoff, fs, order):
    """ This functions apply a butter lowpass filter to a signal
    
        :param data: ECG signal
        :type data: list
        :param cutoff: cutoff frequency
        :type cutoff: float
        :param cutoff: cutoff frequency
        :type cutoff: float
        :param fs: samplerate of the signal
        :type fs: float
        :param order: order of the Butter Filter
        :type order: int
        :return: lowpass filtered ECG signal
        :rtype: list
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return(y)
    
def butter_highpass_filter(data, cutoff, fs, order):
    """ This functions apply a butter highpass filter to a signal
    
        :param data: ECG signal
        :type data: list
        :param cutoff: cutoff frequency
        :type cutoff: float
        :param cutoff: cutoff frequency
        :type cutoff: float
        :param fs: samplerate of the signal
        :type fs: float
        :param order: order of the Butter Filter
        :type order: int
        :return: highpass filtered ECG signal
        :rtype: list
    """
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return(y)
