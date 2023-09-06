"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2018-07-19

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import time
import matplotlib.pyplot as plt
import sys
import numpy

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

def get_data(hzAcq,nSamples):
    #declare ctype variables
    hdwf = c_int()
    sts = c_byte()
    rgdSamples = (c_double*nSamples)()
    cAvailable = c_int()
    cLost = c_int()
    cCorrupted = c_int()
    fLost = 0
    fCorrupted = 0

    #print(DWF version
    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    print("DWF Version: "+str(version.value))

    #open device
    print("Opening first device")
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

    if hdwf.value == hdwfNone.value:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(str(szerr.value))
        print("failed to open device")
        quit()

    print("Generating sine wave...")
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_int(1))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcSine)
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(1))
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(2))
    dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1))

    #set up acquisition
    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_int(1))
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))
    dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord)
    dwf.FDwfAnalogInFrequencySet(hdwf, hzAcq)
    dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double(nSamples/hzAcq.value)) # -1 infinite record length

    #wait at least 2 seconds for the offset to stabilize
    #time.sleep(2)

    print("Starting oscilloscope")
    dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

    cSamples = 0

    while cSamples < nSamples:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if cSamples == 0 and (sts == DwfStateConfig or sts == DwfStatePrefill or sts == DwfStateArmed) :
            # Acquisition not yet started.
            continue

        dwf.FDwfAnalogInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
        
        cSamples += cLost.value

        if cLost.value :
            fLost = 1
        if cCorrupted.value :
            fCorrupted = 1

        if cAvailable.value==0 :
            continue

        if cSamples+cAvailable.value > nSamples :
            cAvailable = c_int(nSamples-cSamples)

        dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(rgdSamples, sizeof(c_double)*cSamples), cAvailable) # get channel 1 data
        #dwf.FDwfAnalogInStatusData(hdwf, c_int(1), byref(rgdSamples, sizeof(c_double)*cSamples), cAvailable) # get channel 2 data
        cSamples += cAvailable.value

    dwf.FDwfAnalogOutReset(hdwf, c_int(0))
    dwf.FDwfDeviceCloseAll()

    print("Recording done")
    if fLost:
        print("Samples were lost! Reduce frequency")
    if fCorrupted:
        print("Samples could be corrupted! Reduce frequency")

    return rgdSamples

hzAcq = c_double(10000)
nSamples = 10000 ############################################################
n_time_save = 10 ############################################################

for i in range(n_time_save):
    start_time = time.time()
    rgdSamples = get_data(hzAcq,nSamples)
    file_name = f"record_{i}.csv"
    f = open(file_name, "w")
    for v in rgdSamples:
        f.write("%s\n" % v)
    f.close()
    end_time = time.time()    
    print("time",end_time- start_time)