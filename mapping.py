import numpy as np



def serialToParallel(bitstream):

    ans = []
    tmp = ''

    for i in range(len(bitstream)):

        tmp += bitstream[i]

        if (i+1)%2 == 0:

            ans.append(tmp)
            tmp = ''

    return ans


def mapping(bitstream, constellation):

    symbols = []
    if constellation == 'BPSK' or constellation == 'bpsk':

        for x in range(len(bitstream)):

            if bitstream[x] == '0':
                symbols.append(-1)

            elif bitstream[x] == '1':
                symbols.append(1)

    elif constellation == 'QPSK' or constellation == 'qpsk':

        tmpBits = serialToParallel(bitstream)
        

        for x in range(len(tmpBits)):

            if tmpBits[x] == "00":
                symbols.append(-1 - 1j)

            elif tmpBits[x] == "01":

                symbols.append(-1 + 1j)

            elif tmpBits[x] == "11":
                symbols.append(1 + 1j)

            elif tmpBits[x] == '10':
                symbols.append(1 - 1j)

    return symbols


def demaping(symbols, constellation):

    bits = ''
    if constellation == 'BPSK' or constellation == 'bpsk':

        for x in range(len(symbols)):

            if symbols[x] == -1:
                bits += '0'

            elif symbols[x] == 1:
                bits += '1'

    elif constellation == 'QPSK' or constellation == 'qpsk':

        for x in range(len(symbols)):

            if symbols[x] == -1 - 1j:
                bits += '00'

            elif symbols[x] == -1 + 1j:
                bits += '01'

            elif symbols[x] == 1 + 1j:
                bits += '11'

            elif symbols[x] == 1 - 1j:
                bits += '10'

    return bits