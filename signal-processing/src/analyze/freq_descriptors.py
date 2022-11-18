import peakutils #peak detection
import numpy as np #to handle datas
import math #to handle mathematical stuff (example power of 2)
import scipy
from scipy.signal import butter, lfilter, welch, square  #for signal filtering
import matplotlib.pyplot as plt  
    
###############################################################################
#                                                                             #
#                       FREQUENCY DOMAIN FEATURES                             #
#                                                                             #
###############################################################################
""" This section contains all the functions used in frequency analysis """ 


def getMNF(rawEMGPowerSpectrum, frequencies):
    """ Obtain the mean frequency of the EMG signal, evaluated as the sum of 
        product of the EMG power spectrum and the frequency divided by total sum of the spectrum intensity::
            
            MNF = sum(fPj) / sum(Pj) for j = 1 -> M 
            M = length of the frequency bin
            Pj = power at freqeuncy bin j
            fJ = frequency of the spectrum at frequency bin j
        
        * Input: 
            * rawEMGPowerSpectrum: PSD as list
            * frequencies: frequencies of the PSD spectrum as list
        * Output:
            * Mean Frequency of the PSD
            
        :param rawEMGPowerSpectrum: power spectrum of the EMG signal
        :type rawEMGPowerSpectrum: list
        :param frequencies: frequencies of the PSD
        :type frequencies: list
        :return: mean frequency of the EMG power spectrum
        :rtype: float
    """
    a = []
    for i in range(0, len(frequencies)):
        a.append(frequencies[i] * rawEMGPowerSpectrum[i])
    b = sum(rawEMGPowerSpectrum)
    MNF = sum(a) / b
    return(MNF)
    
def getMDF(rawEMGPowerSpectrum, frequencies):
    """ Obtain the Median Frequency of the PSD. 
    
        MDF is a frequency at which the spectrum is divided into two regions with equal amplitude, in other words, MDF is half of TTP feature
        
        * Input: 
            * raw EMG Power Spectrum
            * frequencies
        * Output: 
            * Median Frequency  (Hz)
            
        :param rawEMGPowerSpectrum: power spectrum of the EMG signal
        :type rawEMGPowerSpectrum: list
        :param frequencies: frequencies of the PSD
        :type frequencies: list
        :return: median frequency of the EMG power spectrum
        :rtype: float
    """
    MDP = sum(rawEMGPowerSpectrum) * (1/2)
    for i in range(1, len(rawEMGPowerSpectrum)):
        if(sum(rawEMGPowerSpectrum[0:i]) >= MDP):
            return(frequencies[i])
            
def getPeakFrequency(rawEMGPowerSpectrum, frequencies):
    """ Obtain the frequency at which the maximum peak occur 
    
        * Input:    
            * raw EMG Power Spectrum as list
            * frequencies as list
        * Output:
            * frequency in Hz
            
        :param rawEMGPowerSpectrum: power spectrum of the EMG signal
        :type rawEMGPowerSpectrum: list
        :param frequencies: frequencies of the PSD
        :type frequencies: list
        :return: peakfrequency of the EMG Power spectrum
        :rtype: float
    """
    peakFrequency = frequencies[np.argmax(rawEMGPowerSpectrum)]
    return(peakFrequency)

def getMNP(rawEMGPowerSpectrum):
    """ This functions evaluate the mean power of the spectrum.::
        
            Mean Power = sum(Pj) / M, j = 1 --> M, M = len of the spectrum
        
        * Input: 
            * EMG power spectrum
        * Output: 
            * mean power
            
        :param rawEMGPowerSpectrum: power spectrum of the EMG signal
        :type rawEMGPowerSpectrum: list
        :param frequencies: frequencies of the PSD
        :type frequencies: list
        :return: mean power of the EMG power spectrum
        :rtype: float
    """
    
    MNP = np.mean(rawEMGPowerSpectrum)
    return(MNP)
    
def getTTP(rawEMGPowerSpectrum):
    """ This functions evaluate the aggregate of the EMG power spectrum (aka Zero Spectral Moment)
    
        * Input: 
            * raw EMG Power Spectrum
        * Output: 
            * Total Power
        
        :param rawEMGPowerSpectrum: power spectrum of the EMG signal
        :type rawEMGPowerSpectrum: list
        :param frequencies: frequencies of the PSD
        :type frequencies: list
        :return: total power of the EMG power spectrum
        :rtype: float
    """
    
    TTP = sum(rawEMGPowerSpectrum)
    return(TTP)
        
def getSM(rawEMGPowerSpectrum, frequencies, order):
    """ Get the spectral moment of a spectrum::
        
            SM = sum(fj*(Pj**order)), j = 1 --> M
        
        * Input: 
            * raw EMG Power Spectrum
            * frequencies as list
            * order (int)
        * Output: 
            * SM of order = order
        
        :param rawEMGPowerSpectrum: power spectrum of the EMG signal
        :type rawEMGPowerSpectrum: list
        :param frequencies: frequencies of the PSD
        :type frequencies: list
        :param order: order to the moment
        :type order: int
        :return: Spectral moment of order X of the EMG power spectrum
        :rtype: float
    """
    SMo = []
    for j in range(0, len(frequencies)):
        SMo.append(frequencies[j]*(rawEMGPowerSpectrum[j] ** order))
    SMo = sum(SMo)
    return(SMo)   
    
def getFR(rawEMGPowerSpectrum, frequencies, llc=30, ulc=250, lhc=250,uhc=500):
    """ This functions evaluate the frequency ratio of the power spectrum. 
    
        Cut-off value can be decidec experimentally or from the MNF Feature See: Oskoei, M.A., Hu, H. (2006). GA-based feature subset selection for myoelectric classification.
        
        * Input:
            * raw EMG power spectrum as list,
            * frequencies as list,
            * llc = lower low cutoff
            * ulc = upper low cutoff
            * lhc = lower high cutoff
            * uhc = upper high cutoff
        * Output:
            * Frequency Ratio
            
        :param rawEMGPowerSpectrum: power spectrum of the EMG signal
        :type rawEMGPowerSpectrum: list
        :param frequencies: frequencies of the PSD
        :type frequencies: list
        :param llc: lower cutoff frequency for the low frequency components
        :type llc: float
        :param ulc: upper cutoff frequency for the low frequency components
        :type ulc: float
        :param lhc: lower cutoff frequency for the high frequency components
        :type lhc: float
        :param uhc: upper cutoff frequency for the high frequency components
        :type uhc: float
        :return: frequencies ratio of the EMG power spectrum
        :rtype: float
    """
    frequencies = list(frequencies)
    #First we check for the closest value into the frequency list to the cutoff frequencies
    llc = min(frequencies, key=lambda x:abs(x-llc))
    ulc = min(frequencies, key=lambda x:abs(x-ulc))
    lhc = min(frequencies, key=lambda x:abs(x-lhc))
    uhc = min(frequencies, key=lambda x:abs(x-uhc))
    
    LF = sum([P for P in rawEMGPowerSpectrum[frequencies.index(llc):frequencies.index(ulc)]])
    HF = sum([P for P in rawEMGPowerSpectrum[frequencies.index(lhc):frequencies.index(uhc)]])
    FR = LF / HF
    return(FR)

def getPSR(rawEMGPowerSpectrum,frequencies,n=20,fmin=10,fmax=500):
    """ This function computes the Power Spectrum Ratio of the signal, defined as:
        Ratio between the energy P0 which is nearby the maximum value of the EMG power spectrum and the energy P which is the whole energy of the EMG power spectrum
        
        * Input:
            * EMG power spectrum
            * frequencies as list
            * n = range around f0 to evaluate P0
            * fmin = min frequency
            * fmax = max frequency
        
        :param rawEMGPowerSpectrum: power spectrum of the EMG signal
        :type rawEMGPowerSpectrum: list
        :param frequencies: frequencies of the PSD
        :type frequencies: list
        :param n: range of frequencies around f0 to evaluate
        :type n: int
        :param fmin: min frequency to evaluate
        :type fmin: int
        :param fmax: lmaximum frequency to evaluate
        :type fmax: int
        :return: Power spectrum ratio of the EMG power spectrum
        :rtype: float
    """
    
    frequencies = list(frequencies)
    
    #The maximum peak and frequencies are evaluate using the getPeakFrequency functions
    #First we check for the closest value into the frequency list to the cutoff frequencies
    peakFrequency = getPeakFrequency(rawEMGPowerSpectrum, frequencies)
    f0min = peakFrequency - n
    f0max = peakFrequency + n
    f0min = min(frequencies, key=lambda x:abs(x-f0min))
    f0max = min(frequencies, key=lambda x:abs(x-f0max))
    fmin = min(frequencies, key=lambda x:abs(x-fmin))
    fmax = min(frequencies, key=lambda x:abs(x-fmax))
    
    #here we evaluate P0 and P
    P0 = sum(rawEMGPowerSpectrum[frequencies.index(f0min):frequencies.index(f0max)])
    P = sum(rawEMGPowerSpectrum[frequencies.index(fmin):frequencies.index(fmax)])
    PSR = P0 / P
    
    return(PSR)

def getVCF(SM0,SM1,SM2):
    """This function evaluate the variance of the central freuency of the PSD.::
            
            VCF = (1 / SM0)*sum(Pj*(fj - fc)**2),j = 1 --> M, = SM2 / SM0 - (SM1 /SM0) **2
        
        * Input:
            * SM0: spectral moment of order 0
            * SM1: spectral moment of order 1
            * SM2: spectral moment of order 0
        * Output: 
            * Variance of Central frequency of the Power spectrum
            
        :param SM0: Spectral moment of order 0
        :type SM0: float
        :param SM1: Spectral moment of order 1
        :type SM1: float
        :param SM2: Spectral moment of order 2
        :type SM2: float
        :return: Variance of central frequency
        :rtype: float
    """
    VCF = (SM2 / SM0) - (SM1/SM0)**2
    return(VCF)
    
###############################################################################
#                                                                             #
#                           PREPROCESSING                                     #
#                                                                             #
###############################################################################  

def phasicFilter(rawEMGSignal,samplerate, seconds=4):
    """ Apply a phasic filter to the signal, with +-4 seconds from each sample
        
        * Input:
            * rawEMGSignal = emg signal as list
            * samplerate = samplerate of the signal    
        * Output:
            * phasic filtered signal   
        
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param samplerate: samplerate of the signal in Hz
        :type samplerate: int 
        :return: the phasic filtered signal
        :rtype: list
    """
    phasicSignal = []    
    for sample in range(0,len(rawEMGSignal)):
        smin = sample - 4 * samplerate #min sample index
        smax = sample + 4 * samplerate #max sample index
        #is smin is < 0 or smax > signal length, fix it to the closest real sample
        if(smin < 0): 
            smin = sample
        if(smax > len(rawEMGSignal)):
            smax = sample
        #substract the mean of the segment
        newsample = rawEMGSignal[sample] - np.median(rawEMGSignal[smin:smax])
        #move to th
        phasicSignal.append(newsample)
    return(phasicSignal)
    
def getPSD(rawEMGSignal, samplerate):
    frequencies, psd = welch(rawEMGSignal, fs=samplerate,
               window='hann',   # apply a Hanning window before taking the DFT
               nperseg=256,        # compute periodograms of 256-long segments of x
               detrend='constant',scaling="spectrum") # detrend x by subtracting the mean
    return([psd,frequencies])  
