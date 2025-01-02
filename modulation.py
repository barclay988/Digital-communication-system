import numpy as np
from scipy.fft import fft, ifft




def addCyclicPrefix(data,cp):

    return np.hstack([data[len(data) - cp:], data])


def removeCyclicPrefix(data,cp):

       return data[cp:]


def groupSymbols(symbols,size):

    tmpSymbols = []
    groupedSymbols = []

    for i in range(len(symbols)):

        tmpSymbols.append(symbols[i])

        if (i+1)% size == 0:

            groupedSymbols.append(tmpSymbols)
            tmpSymbols = []

    return groupedSymbols




def preamblesCreation():

    qpskSymbols = [-1 + 1j, 1 - 1j, 1 + 1j, -1 - 1j]

    storePreambles = [qpskSymbols[(i) % len(qpskSymbols)] for i in range(32)]

    storePreambles = np.array(storePreambles)

    storePreambles = np.sqrt(2) * storePreambles

    storePreambles[::2] = 0

    storePreambles = np.fft.ifft(storePreambles)

    tmpPream = addCyclicPrefix(storePreambles, 16)

    storePreambles = np.concatenate((tmpPream, storePreambles))

    return storePreambles


def allocateSubcarriers(symbols):


    OFDMsymbol = [0+0j for i in range(64)]
    OFDMsymbol = np.array(OFDMsymbol)


    pilotCarriers = np.array([43, 57, 7, 21])

    nullCarriers = np.array([32, 33, 34, 35, 36, 37, 0, 27, 28, 29, 30, 31])


    dataCarriers = np.array([38, 39, 40, 41, 42, 44, 45, 46,
                  47, 48, 49, 50, 51, 52, 53, 54,
                  55, 56, 58, 59, 60, 61, 62, 63,
                  1, 2, 3, 4, 5, 6, 8, 9, 10, 11,
                  12, 13, 14, 15, 16, 17, 18, 19,
                  20, 22, 23, 24, 25, 26])
    

    OFDMsymbol[(pilotCarriers)] = 1+0j
    OFDMsymbol[(nullCarriers)] = 0
    OFDMsymbol[(dataCarriers)] = symbols


    OFDMsymbol =  np.fft.fft(OFDMsymbol)

    OFDMsymbol = addCyclicPrefix(OFDMsymbol, 16)

    return OFDMsymbol


def OFDMmodulation(symbols,symbolSize,n):


    groupedSymbols = groupSymbols(symbols,n)


    OFDMsymbols = []

    for i in range(len(groupedSymbols)):

        OFDMsymbols.append(allocateSubcarriers(groupedSymbols[i]).tolist())


    preambles = preamblesCreation()

    preambles = preambles.tolist()


    tmp = []

    OFDMframe = []

    for i in range(len(OFDMsymbols)):

        OFDMframe += OFDMsymbols[i]


    OFDMframe = preambles + OFDMframe


    return OFDMframe


def upconvertion(signal,freq):

    t = np.arange(len(signal))

    return signal * np.exp(2j * np.pi * freq * t)



def downconvertion(signal,freq):
    
    t = np.arange(len(signal))

    return signal * np.exp(-2j * np.pi * freq * t)