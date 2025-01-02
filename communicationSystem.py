import numpy as np
import random
from scipy.fft import fft, ifft
import encoding
import mapping
import modulation
import channelEstimation
import synchronization



def generateBits(num):

    bits = [] 

    for i in range(num):

        bits.append(random.choice(['0','1']))

    return bits



def applyNoise(signal, snr):

    sig = 1 / np.sqrt(pow(10, snr / 10) * 2 * 2)

    vari = 0.01

    wn = sig * np.random.normal(0, vari, len(signal)) + sig * np.random.normal(0, vari, len(signal)) * 1j

    return signal + wn


def splitOFDMframe(signal):
     
     newSymbols = modulation.groupSymbols(signal,80)

     return newSymbols

def removeCP(symbols):
     
    newSymbol = []

    for i in range(len(symbols)):

        tmp =  np.fft.ifft(modulation.removeCyclicPrefix(symbols[i],16))

        newSymbol.append(tmp)


    return newSymbol


def equalizeSymbols(symbols):

    newSymbols = []

    for i in range(len(symbols)):

        estimated = channelEstimation.channelEstimation(symbols[i])

        equalized = channelEstimation.channelEqualization(symbols[i],estimated)

        newSymbols.append(equalized)

    return newSymbols


def retriveSymbols(symbols, cons):

    newSymbols = []

    for i in range(len(symbols)):

        newSymbols.append(hardDecision(symbols[i],cons))


    return newSymbols


def hardDecision(signalData, cons):

    if cons == 'qpsk' or cons == 'QPSK':
     symbols = np.array([-1 - 1j, -1 + 1j, 1 + 1j, 1 - 1j])

    else:
        symbols = np.array([-1 , 1 ])

    ans = []
    tmp = []

    for i in range(len(signalData)):

        if cons == 'qpsk' or cons == 'QPSK':

            tmp.append(np.abs(signalData[i] - symbols[0])**2)
            tmp.append(np.abs(signalData[i] - symbols[1])**2)
            tmp.append(np.abs(signalData[i] - symbols[2])**2)
            tmp.append(np.abs(signalData[i] - symbols[3])**2)

        else:

            tmp.append(np.abs(signalData[i] - symbols[0]) ** 2)
            tmp.append(np.abs(signalData[i] - symbols[1]) ** 2)



        minVal = tmp.index(min(tmp))
        ans.append(symbols[minVal])
        tmp = []

    return ans


def extractBits(symbols,cons):


    newBits = ''

    for i in range(len(symbols)):

        tmp = mapping.demaping(symbols[i],cons)

        newBits += tmp

    return newBits



def BERcalculation(origBits, retrvBits):


   errs = 0

   for i in range(len(origBits)):

       if retrvBits[i] != origBits[i]:

           errs += 1

   return errs/len(origBits)

     



def transmitter(inputBits, cons, freq, SNR):


    codeBits = encoding.convolutionalEncoder(inputBits)

    print("bits: ", len(codeBits))
    print()

    inputSymbols = mapping.mapping(codeBits,cons)

    print("symbols: ", len(inputSymbols))
    print()


    nSymbols = len(inputSymbols) // 48

    modulatedSignal = modulation.OFDMmodulation(inputSymbols, nSymbols, 48)

    print("modulated: ", len(modulatedSignal[0]))
    print()

   

    modulatedSignal = modulation.upconvertion(modulatedSignal,freq)

    print("upconverted: ", len(modulatedSignal[0]))
    print()


    storePreambles = modulatedSignal[0][:80].tolist()


    with open("preambles.txt", "w") as file:
                
                for value in storePreambles:

                    file.write(f"{value}\n")

    STO = 280

    CFO = 0.3
    modulatedSignal = synchronization.applySTO(modulatedSignal, STO)
        
    modulatedSignal = synchronization.applyCFO(modulatedSignal, CFO, 64)

    SNR = 6

    txSignal = applyNoise(modulatedSignal,SNR)

    return modulatedSignal



def receiver(txSignal, cons,  freq):

    signal = txSignal[0] 

    # print("signal:",len(signal))
    # print()

    # exit()

    with open("preambles.txt", "r") as file:
                    
            initPreambles = [complex(line.strip()) for line in file]

    initPreambles = np.array(initPreambles)


    # exit()
        
    rxSignal = synchronization.removeSTO(signal,initPreambles)

    print("after STO: ", len(rxSignal))
    print()

    rxSignal = modulation.downconvertion(rxSignal,freq)

    print("fter downconvertion: ", len(rxSignal))
    print()


    estCFO = synchronization.estimateCFO(rxSignal,32)

   

    rxSignal = synchronization.removeCFO(rxSignal,estCFO,64)

    print("fter CFO: ", len(rxSignal))
    print()


    exit()

    rxSignal = rxSignal[80:]

    print("without preambles: ", len(rxSignal))
    print()

    smOFDM = splitOFDMframe(rxSignal)

    print("getOFDMsymbs: ", len(smOFDM[0]))
    print()

        # also does FFT
    smOFDM = removeCP(smOFDM)

    print("no GI and FFT'd: ", len(smOFDM[0]))
    print()

        #
    smOFDM = equalizeSymbols(smOFDM)

    print("removed Channel: ", len(smOFDM[0]))
    print()

    symIN = retriveSymbols(smOFDM, cons)

    print("hd dcn: ", len(symIN[0]))
    print()

    symIN = extractBits(symIN, cons)

    print("demapped: ", len(symIN))
    print()
   

    ans = encoding.ViterbiDecoder(symIN)

    return ans




def main():


    nBits = 18504

    cons = 'BPSK'

    freq = 4000

    SNR = 10

    inputBits = generateBits(nBits)

    print("inputBits: ", len(inputBits))
    print()

    signalData = transmitter(inputBits, cons, freq, SNR)

    outBits = receiver(signalData,cons,freq)

    ber = BERcalculation(inputBits,outBits)

    print("BER: ", ber)
    print()
    

if __name__ == "__main__":
    main()





