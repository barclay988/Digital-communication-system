import numpy as np


def applyCFO(signal, cfo, Ns):

    cfo = cfo / Ns

    t = np.arange(len(signal))

    return signal *  np.exp(2j * np.pi * cfo * t )



def removeCFO(signal, cfo, Ns):

    t = np.arange(len(signal))

    return signal *  np.exp(-2j * np.pi * cfo * t / Ns)



def applySTO(signal, sto):

    return  np.hstack([np.zeros(sto), signal])


def removeSTO(signal,preambles):

        result = np.correlate(signal, preambles)

        sto = np.argmax(np.abs(result))

        print("sto: ", sto)
        print()


        return signal[sto:]



def estimateCFO(signal, num):

    preambles = np.arange(0, 64)

    P1 = np.zeros(len(preambles), dtype=complex)

    for i, d in enumerate(preambles):

        P1[i] = sum(np.conj(signal[d + m]) * signal[d + m + num] for m in range(num))

    R1 = np.zeros(len(preambles))

    for i, d in enumerate(preambles):
      
        R1[i] = sum(np.abs(signal[d + m + num]) ** 2 for m in range(num))

    M = np.abs(P1) ** 2 / R1 ** 2

    maxIndex = np.argmax(M[:80])

    angleP = np.angle(P1)

    cfo = angleP[maxIndex] / np.pi

    return cfo


