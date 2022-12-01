from .freq_descriptors import * 
from .time_descriptors import * 
from .filters import * 


def analyzeEMG(rawEMGSignal, samplerate, preprocessing=True,lowpass=50,highpass=20,threshold = 0.01 ,nseg=3,phasic_seconds=4):
    
    """ This functions acts as entrypoint for the EMG Analysis.
    
        * Input:
            * rawEMGSignal = raw signal as list
            * samplerate = samplerate of the signal
            * lowpass = lowpass cutoff in Hz
            * highpass = highpass cutoff in Hz
            * threshold for the evaluation of ZC,MYOP,WAMP,SSC
            * nseg = number of segments for MAVSLPk, MHW,MTW
        * Output:
            * results dictionary
            
    """ 
    resultsdict = {"TimeDomain":{},"FrequencyDomain":{}}
    
    if(preprocessing):
        #Preprocessing
        filteredEMGSignal = butter_lowpass_filter(rawEMGSignal, lowpass, samplerate, 2)#filter the signal with a cutoff at 1Hz and a 2th order Butterworth filter
        filteredEMGSignal = butter_highpass_filter(filteredEMGSignal, highpass, samplerate, 2)#filter the signal with a cutoff at 0.05Hz and a 2th order Butterworth filter
        filteredEMGSignal = phasicFilter(filteredEMGSignal, samplerate,seconds=phasic_seconds)
    else:
        filteredEMGSignal = rawEMGSignal
    
    #Time Domain Analysis
    resultsdict["TimeDomain"]["IEMG"] = getIEMG(filteredEMGSignal)
    resultsdict["TimeDomain"]["MAV"] = getMAV(filteredEMGSignal)
    resultsdict["TimeDomain"]["MAV1"] = getMAV1(filteredEMGSignal)
    resultsdict["TimeDomain"]["MAV2"] = getMAV2(filteredEMGSignal)
    resultsdict["TimeDomain"]["SSI"] = getSSI(filteredEMGSignal)
    resultsdict["TimeDomain"]["VAR"] = getVAR(filteredEMGSignal)
    resultsdict["TimeDomain"]["TM3"] = getTM(filteredEMGSignal,3)
    resultsdict["TimeDomain"]["TM4"] = getTM(filteredEMGSignal,4)
    resultsdict["TimeDomain"]["TM5"] = getTM(filteredEMGSignal,5)
    resultsdict["TimeDomain"]["LOG"] = getLOG(filteredEMGSignal)
    resultsdict["TimeDomain"]["RMS"] = getRMS(filteredEMGSignal)
    resultsdict["TimeDomain"]["WL"] = getWL(filteredEMGSignal)
    resultsdict["TimeDomain"]["AAC"] = getAAC(filteredEMGSignal)
    resultsdict["TimeDomain"]["DASDV"] = getDASDV(filteredEMGSignal)
    resultsdict["TimeDomain"]["AFB"] = getAFB(filteredEMGSignal,samplerate)
    resultsdict["TimeDomain"]["ZC"] = getZC(filteredEMGSignal,threshold)
    resultsdict["TimeDomain"]["MYOP"] = getMYOP(filteredEMGSignal,threshold)
    resultsdict["TimeDomain"]["WAMP"] = getWAMP(filteredEMGSignal,threshold)
    resultsdict["TimeDomain"]["SSC"] = getSSC(filteredEMGSignal,threshold)
    # resultsdict["TimeDomain"]["MAVSLPk"] = getMAVSLPk(filteredEMGSignal,nseg)
    # resultsdict["TimeDomain"]["HIST"] = getHIST(filteredEMGSignal,threshold=threshold)
    
    #Frequency Domain Analysis
    rawEMGPowerSpectrum, frequencies = getPSD(filteredEMGSignal,samplerate)
    resultsdict["FrequencyDomain"]["MNF"] = getMNF(rawEMGPowerSpectrum, frequencies)
    resultsdict["FrequencyDomain"]["MDF"] = getMDF(rawEMGPowerSpectrum, frequencies)
    resultsdict["FrequencyDomain"]["PeakFrequency"] = getPeakFrequency(rawEMGPowerSpectrum, frequencies)
    resultsdict["FrequencyDomain"]["MNP"] = getMNP(rawEMGPowerSpectrum)
    resultsdict["FrequencyDomain"]["TTP"] = getTTP(rawEMGPowerSpectrum)
    resultsdict["FrequencyDomain"]["SM1"] = getSM(rawEMGPowerSpectrum,frequencies,1)
    resultsdict["FrequencyDomain"]["SM2"] = getSM(rawEMGPowerSpectrum,frequencies,2)
    resultsdict["FrequencyDomain"]["SM3"] = getSM(rawEMGPowerSpectrum,frequencies,3)
    resultsdict["FrequencyDomain"]["FR"] = getFR(rawEMGPowerSpectrum,frequencies)
    resultsdict["FrequencyDomain"]["PSR"] = getPSR(rawEMGPowerSpectrum,frequencies)
    resultsdict["FrequencyDomain"]["VCF"] = getVCF(resultsdict["FrequencyDomain"]["TTP"],resultsdict["FrequencyDomain"]["SM1"],resultsdict["FrequencyDomain"]["SM2"])
    
    return(resultsdict)