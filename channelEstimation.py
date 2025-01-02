import numpy as np
import scipy



def channelEstimation(signal):

   
    pilotIndices = np.array([ 43, 57, 7, 21])

    pilotSymbols = np.array([1 +0j,1 +0j,1 +0j,1 +0j])

    signal = np.array(signal)

    tmpSymbols = signal[pilotIndices]

    return tmpSymbols / pilotSymbols


def doInterpolation(estimate, pilotIndexes, dataVal):


    channR = np.array(estimate)
    indexPs = np.array(pilotIndexes)
    vals = np.array(dataVal)
    ans = np.zeros_like(vals)

    for count, val1 in enumerate(vals):

        if val1 > channR[0] and val1 < channR[-1]:

            for ind in range(len(channR) - 1):

                if channR[ind] <= val1 < channR[ind + 1]:
                    a = (indexPs[ind + 1] - indexPs[ind]) * (val1 - channR[ind])
                    b = (channR[ind + 1] - channR[ind])

                    ans[count] = indexPs[ind] + a / b

                    break

        elif val1 <= channR[0]:
            ans[count] = indexPs[0]

        else:
            ans[count] = indexPs[-1]

    return ans




def channelEqualization(signalData, effect):



    carr = np.array([38, 39, 40, 41, 42, 44, 45, 46,
                  47, 48, 49, 50, 51, 52, 53, 54,
                  55, 56, 58, 59, 60, 61, 62, 63,
                  1, 2, 3, 4, 5, 6, 8, 9, 10, 11,
                  12, 13, 14, 15, 16, 17, 18, 19,
                  20, 22, 23, 24, 25, 26])

    posP1 = np.array([43, 57, 7, 21])


    pls = 1 + 0j

    pilotSymbols = np.array([pls, pls, pls, pls])

    signalData = np.array(signalData)

    origData = signalData[carr]

    origData = signalData[:]

    nEffect = doInterpolation(effect,pilotSymbols,origData)

    ans = signalData / nEffect

    ans = ans[carr]

    return ans