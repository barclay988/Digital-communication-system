import numpy as np
from viterbi import Viterbi




def ViterbiDecoder(bitsream):

    bitsream = [int(i) for i in bitsream]
    vert = Viterbi(3, [0o7, 0o5])

    ans = vert.decode(bitsream)

    ans = [str(i) for i in ans]

    ans = ''.join(ans)

    return ans


def convolutionalEncoder(bitsream):

    bitsream = [int(i) for i in bitsream]
    vert = Viterbi(3, [0o7, 0o5])

    ans = vert.encode(bitsream)

    ans = [str(i) for i in ans]

    ans = ''.join(ans)

    return ans





# initBits = '11010'


# encoded = convolutionalEncoder(initBits)

# print("encoded: ", encoded)
# print()


# decoded = ViterbiDecoder(encoded)

# print("decoded: ", decoded)
# print()