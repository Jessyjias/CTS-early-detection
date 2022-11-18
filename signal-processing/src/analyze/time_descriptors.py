import peakutils #peak detection
import numpy as np #to handle datas
import math #to handle mathematical stuff (example power of 2)
import scipy
from scipy.signal import butter, lfilter, welch, square  #for signal filtering
import matplotlib.pyplot as plt

###############################################################################
#                                                                             #
#                       TIME DOMAIN FEATURES                                  #
#                                                                             #
###############################################################################
""" Features have been taken from: Phinyomark, A., Phukpattaranont, P., & Limsakul, C. (2012). """

def getIEMG(rawEMGSignal):
    """ This function compute the sum of absolute values of EMG signal Amplitude.::
        
            IEMG = sum(|xi|) for i = 1 --> N
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * integrated EMG    
        
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: the IEMG of the EMG Signal
        :rtype: float
    """
    
    IEMG = np.sum([abs(x) for x in rawEMGSignal])    
    return(IEMG)
    
def getMAV(rawEMGSignal):
    """ Thif functions compute the  average of EMG signal Amplitude.::
        
            MAV = 1/N * sum(|xi|) for i = 1 --> N
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * Mean Absolute Value    
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: the MAV of the EMG Signal
        :rtype: float
    """
    
    MAV = 1/len(rawEMGSignal) *  np.sum([abs(x) for x in rawEMGSignal])    
    return(MAV)
    
def getMAV1(rawEMGSignal):
    """ This functoin evaluate Average of EMG signal Amplitude, using the modified version n°.1.::
        
            IEMG = 1/N * sum(wi|xi|) for i = 1 --> N
            wi = {
                  1 if 0.25N <= i <= 0.75N,
                  0.5 otherwise
                  }
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * Mean Absolute Value   
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: the MAV (modified version n. 1)  of the EMG Signal
        :rtype: float
    """
    wIndexMin = int(0.25 * len(rawEMGSignal))
    wIndexMax = int(0.75 * len(rawEMGSignal))
    absoluteSignal = [abs(x) for x in rawEMGSignal]
    IEMG = 0.5 * np.sum([x for x in absoluteSignal[0:wIndexMin]]) + np.sum([x for x in absoluteSignal[wIndexMin:wIndexMax]]) + 0.5 * np.sum([x for x in absoluteSignal[wIndexMax:]])
    MAV1 = IEMG / len(rawEMGSignal)
    return(MAV1)
    
def getMAV2(rawEMGSignal):
    """ This functoin evaluate Average of EMG signal Amplitude, using the modified version n°.2.::
        
            IEMG = 1/N * sum(wi|xi|) for i = 1 --> N
            wi = {
                  1 if 0.25N <= i <= 0.75N,
                  4i/N if i < 0.25N
                  4(i-N)/N otherwise
                  }
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * Mean Absolute Value 
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: the MAV (modified version n. 2)  of the EMG Signal
        :rtype: float
    """
    
    N = len(rawEMGSignal)
    wIndexMin = int(0.25 * N) #get the index at 0.25N
    wIndexMax = int(0.75 * N)#get the index at 0.75N

    temp = [] #create an empty list
    for i in range(0,wIndexMin): #case 1: i < 0.25N
        x = abs(rawEMGSignal[i] * (4*i/N))
        temp.append(x)
    for i in range(wIndexMin,wIndexMax+1): #case2: 0.25 <= i <= 0.75N
        x = abs(rawEMGSignal[i])
        temp.append(x)
    for i in range(wIndexMax+1,N): #case3; i > 0.75N
        x = abs(rawEMGSignal[i]) * (4*(i - N) / N)
        temp.append(x)
        
    MAV2 = np.sum(temp) / N
    return(MAV2)

def getSSI(rawEMGSignal):
    """ This function compute the summation of square values of the EMG signal.::
        
            SSI = sum(xi**2) for i = 1 --> N

        * Input: 
            * raw EMG Signal as list
        * Output: 
            * Simple Square Integral
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: SSI of the signal
        :rtype: float
    """
    
    SSI = np.sum([x**2 for x in rawEMGSignal])
    return(SSI)    
    
def getVAR(rawEMGSignal):
    """ Summation of average square values of the deviation of a variable.::
        
            VAR = (1 / (N - 1)) * sum(xi**2) for i = 1 --> N

        * Input: 
            * raw EMG Signal as list
        * Output: 
            * Summation of the average square values
        
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: the VAR of the EMG Signal
        :rtype: float
    """
    
    SSI = np.sum([x**2 for x in rawEMGSignal])
    N = len(rawEMGSignal)
    VAR = SSI* (1 / (N - 1))
    return(VAR)    
    
def getTM(rawEMGSignal, order):
    """ 
        This function compute the Temporal Moment of order X of the EMG signal.::
        
            TM = (1 / N * sum(xi**order) for i = 1 --> N
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * TM of order = order
        
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param order: order the the TM function 
        :type order: int
        :return: Temporal Moment of order X of the EMG signal
        :rtype: float
    """
    N = len(rawEMGSignal)
    TM = abs((1/N) * np.sum([x**order for x in rawEMGSignal]))
    
    return(TM)    
    
def getRMS(rawEMGSignal):
    """ Get the root mean square of a signal.::
        
            RMS = (sqrt( (1 / N) * sum(xi**2))) for i = 1 --> N
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * Root mean square of the signal
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: Root mean square of the EMG signal
        :rtype: float
        
        
    """
    N = len(rawEMGSignal)
    RMS = np.sqrt((1/N) * np.sum([x**2 for x in rawEMGSignal]))
    
    return(RMS)   
def getLOG(rawEMGSignal):
    """ LOG is a feature that provides an estimate of the muscle contraction force.::
        
            LOG = e^((1/N) * sum(|xi|)) for x i = 1 --> N
        
        * Input: 
            * raw EMG Signal
        * Output = * LOG    
        
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: LOG feature of the EMG Signal
        :rtype: float
    """
    LOG = math.exp( (1/len(rawEMGSignal)) * sum([abs(x) for x in rawEMGSignal]))    
    
    return(LOG)

def getWL(rawEMGSignal):
    """ Get the waveform length of the signal, a measure of complexity of the EMG Signal.::
            
            WL = sum(|x(i+1) - xi|) for i = 1 --> N-1
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * wavelength of the signal
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: Waveform length of the signal
        :rtype: float
    """
    N = len(rawEMGSignal)
    temp = []    
    for i in range(0,N-1):
        temp.append(abs(rawEMGSignal[i+1] - rawEMGSignal[i]))
    WL = sum(temp)
    return(WL)   
    
def getAAC(rawEMGSignal):
    """ Get the Average amplitude change.::
        
            AAC = 1/N * sum(|x(i+1) - xi|) for i = 1 --> N-1
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * Average amplitude change of the signal
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: Average Amplitude Change of the signal
        :rtype: float
    """
    N = len(rawEMGSignal)
    WL = getWL(rawEMGSignal)
    ACC = 1/N * WL
    return(ACC)
    
def getDASDV(rawEMGSignal):
    """ Get the standard deviation value of the the wavelength.::
        
            DASDV = sqrt( (1 / (N-1)) * sum((x[i+1] - x[i])**2 ) for i = 1 --> N - 1    
        
        * Input: 
            * raw EMG Signal
        * Output:
            * DASDV
            
                    
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: standard deviation value of the the wavelength
        :rtype: float
    """
    
    N = len(rawEMGSignal)
    temp = []    
    for i in range(0,N-1):
        temp.append((rawEMGSignal[i+1] - rawEMGSignal[i])**2)
    DASDV = (1 / (N - 1)) * sum(temp)
    return(DASDV)

def getAFB(rawEMGSignal,samplerate, windowSize=32):
    """ Get the amplitude at first Burst.
    
        Reference: Du, S., & Vuskovic, M. (2004, November). Temporal vs. spectral approach to feature extraction from prehensile EMG signals. In Information Reuse and Integration, 2004. IRI 2004. Proceedings of the 2004 IEEE International Conference on (pp. 344-350). IEEE.
        
        * Input: 
            * rawEMGSignal as list
            * samplerate of the signal in Hz (sample / s)
            * windowSize = window size in ms
        * Output: 
            * amplitude at first burst
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param samplerate: samplerate of the signal int Hz
        :type samplerate: int
        :param windowSize: window size in ms to use for the analysis
        :type windowsSize: int
        :return: Amplitute ad first Burst
        :rtype: float
    """
    squaredSignal = square(rawEMGSignal) #squaring the signal
    windowSample = int((windowSize * 1000) / samplerate) #get the number of samples for each window
    w = np.hamming(windowSample)
    #From: http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
    filteredSignal = np.convolve(w/w.sum(),squaredSignal,mode='valid')
    peak = peakutils.indexes(filteredSignal)[0]
    AFB = filteredSignal[peak]
    return(AFB)
              
    
def getZC(rawEMGSignal, threshold):
    """ How many times does the signal crosses the 0 (+-threshold).::
        
            ZC = sum([sgn(x[i] X x[i+1]) intersecated |x[i] - x[i+1]| >= threshold]) for i = 1 --> N - 1
            sign(x) = {
                        1, if x >= threshold
                        0, otherwise
                    }
        
        * Input:
            * rawEMGSignal = EMG signal as list
            * threshold = threshold to use in order to avoid fluctuations caused by noise and low voltage fluctuations
        * Output:
            * ZC index       
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param threshold: value to sum / substract to the zero when evaluating the crossing.
        :type threshold: int
        :return: Number of times the signal crosses the 0 (+- threshold)
        :rtype: float
    """
    positive = (rawEMGSignal[0] > threshold)
    ZC = 0
    for x in rawEMGSignal[1:]:
        if(positive):
            if(x < 0 -threshold):
                positive = False
                ZC += 1
        else:
            if(x > 0 + threshold):
                positive = True
                ZC += 1
    return(ZC)
    
def getMYOP(rawEMGSignal, threshold):
    """ The myopulse percentage rate (MYOP) is an average value of myopulse output.
        It is defined as one absolute value of the EMG signal exceed a pre-defined thershold value. ::
        
            MYOP = (1/N) * sum(|f(xi)|) for i = 1 --> N
            f(x) = {
                    1 if x >= threshold
                    0 otherwise
            }
        
        * Input:
            * rawEMGSignal = EMG signal as list
            * threshold = threshold to avoid fluctuations caused by noise and low voltage fluctuations
        * Output:
            * Myopulse percentage rate
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param threshold: value to sum / substract to the zero when evaluating the crossing.
        :type threshold: int
        :return: Myopulse percentage rate of the signal
        :rtype: float
    """
    N = len(rawEMGSignal)
    MYOP = len([1 for x in rawEMGSignal if abs(x) >= threshold]) / N
    return(MYOP)
    
def getWAMP(rawEMGSignal, threshold):
    """ Wilson or Willison amplitude is a measure of frequency information.
        It is a number of time resulting from difference between the EMG signal of two adjoining segments, that exceed a threshold.::
            
            WAMP = sum( f(|x[i] - x[i+1]|)) for n = 1 --> n-1
            f(x){
                1 if x >= threshold
                0 otherwise
            }
        
        * Input:
            * rawEMGSignal = EMG signal as list
            * threshold = threshold to avoid fluctuations caused by noise and low voltage fluctuations
        * Output:
            * Wilson Amplitude value
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param threshold: value to sum / substract to the zero when evaluating the crossing.
        :type threshold: int
        :return: Willison amplitude 
        :rtype: float
    """
    
    N = len(rawEMGSignal)
    WAMP = 0
    for i in range(0,N-1):
        x = rawEMGSignal[i] - rawEMGSignal[i+1]
        if(x >= threshold):
            WAMP += 1
    return(WAMP)
    
def getSSC(rawEMGSignal,threshold):
    """ Number of times the slope of the EMG signal changes sign.::
        
            SSC = sum(f( (x[i] - x[i-1]) X (x[i] - x[i+1]))) for i = 2 --> n-1
            
            f(x){
                1 if x >= threshold
                0 otherwise
            }
           
        * Input: 
            * raw EMG Signal
        * Output: 
            * number of Slope Changes
        
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param threshold: value to sum / substract to the zero when evaluating the crossing.
        :type threshold: int
        :return: Number of slope's sign changes
        :rtype: int
    """
    
    N = len(rawEMGSignal)
    SSC = 0
    for i in range(1,N-1):
        a,b,c = [rawEMGSignal[i-1],rawEMGSignal[i],rawEMGSignal[i+1]]
        if(a + b + c >= threshold *3 ): #computed only if the 3 values are above the threshold
            if(a < b > c or a > b < c ): #if there's change in the slope
                SSC += 1
    return(SSC)
    
def getMAVSLPk(rawEMGSignal, nseg):
    """ Mean Absolute value slope is a modified versions of MAV feature.
    
        The MAVs of adiacent segments are determinated. ::
            
            MAVSLPk = MAV[k+1] - MAV[k]; k = 1,..,k+1
        
        * Input: 
            * raw EMG signal as list
            * nseg = number of segments to evaluate
                
        * Output: 
             * list of MAVs
        
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param nseg: number of segments to evaluate
        :type nseg: int
        :return: Mean absolute slope value
        :rtype: float
    """
    N = len(rawEMGSignal)
    lenK = int(N / nseg) #length of each segment to compute
    MAVSLPk = []
    for s in range(0,N,lenK):
        MAVSLPk.append(getMAV(rawEMGSignal[s:s+lenK]))
    return(MAVSLPk)    


def getHIST(rawEMGSignal,nseg=9,threshold=50):
    """ Histograms is an extension version of ZC and WAMP features. 
    
        * Input:
            * raw EMG Signal as list
            * nseg = number of segment to analyze
            * threshold = threshold to use to avoid DC fluctuations
            
        * Output:
            * get zc/wamp for each segment
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :param nseg: number of segments to analyze
        :type nseg: int
        :param threshold: value to sum / substract to the zero when evaluating the crossing.
        :type threshold: int
        :return: Willison amplitude 
        :rtype: float
    """
    segmentLength = int(len(rawEMGSignal) / nseg)
    HIST = {}
    for seg in range(0,nseg):
        HIST[seg+1] = {}
        thisSegment = rawEMGSignal[seg * segmentLength: (seg+1) * segmentLength]
        HIST[seg+1]["ZC"] = getZC(thisSegment,threshold)
        HIST[seg+1]["WAMP"] = getWAMP(thisSegment,threshold)
    return(HIST)