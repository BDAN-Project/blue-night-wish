from components import *

printing = False


# Message expansion function 1
def expand32_1(i, M32, H, Q):
    return (
            s32_1(Q[i - 16]) + s32_2(Q[i - 15]) + s32_3(Q[i - 14]) + s32_0(Q[i - 13])
            + s32_1(Q[i - 12]) + s32_2(Q[i - 11]) + s32_3(Q[i - 10]) + s32_0(Q[i - 9])
            + s32_1(Q[i - 8]) + s32_2(Q[i - 7]) + s32_3(Q[i - 6]) + s32_0(Q[i - 5])
            + s32_1(Q[i - 4]) + s32_2(Q[i - 3]) + s32_3(Q[i - 2]) + s32_0(Q[i - 1])
            + ((i * 0x05555555 + rotl32(M32[(i - 16) % 16], ((i - 16) % 16) + 1)
                + rotl32(M32[(i - 13) % 16], ((i - 13) % 16) + 1)
                - rotl32(M32[(i - 6) % 16], ((i - 6) % 16) + 1)) ^ H[(i - 16 + 7) % 16])
    )


# Message expansion function 2
def expand32_2(i, M32, H, Q):
    return (
            Q[i - 16] + r32_01(Q[i - 15]) + Q[i - 14] + r32_02(Q[i - 13])
            + Q[i - 12] + r32_03(Q[i - 11]) + Q[i - 10] + r32_04(Q[i - 9])
            + Q[i - 8] + r32_05(Q[i - 7]) + Q[i - 6] + r32_06(Q[i - 5])
            + Q[i - 4] + r32_07(Q[i - 3]) + s32_4(Q[i - 2]) + s32_5(Q[i - 1])
            + ((i * 0x05555555 + rotl32(M32[(i - 16) % 16], ((i - 16) % 16) + 1)
                + rotl32(M32[(i - 13) % 16], ((i - 13) % 16) + 1)
                - rotl32(M32[(i - 6) % 16], ((i - 6) % 16) + 1)) ^ H[(i - 16 + 7) % 16])
    )


def Compression256(M32, H):
    W = np.zeros(16, dtype=np.uint32)
    Q = np.zeros(32, dtype=np.uint32)
    if printing:
        [print(f'M{i} = ', hex(M32[i])) for i in range(16)]

    # This part is the function f0 - in the documentation

    # First we mix the message block *M32 (M in the documentation)
    # with the previous double pipe *H.
    # For a fixed previous double pipe, or fixed message block, this
    # part is bijection.
    # This transformation diffuses every one bit difference in 5 words
    W[0] = (M32[5] ^ H[5]) - (M32[7] ^ H[7]) + (M32[10] ^ H[10]) + (M32[13] ^ H[13]) + (M32[14] ^ H[14])
    W[1] = (M32[6] ^ H[6]) - (M32[8] ^ H[8]) + (M32[11] ^ H[11]) + (M32[14] ^ H[14]) - (M32[15] ^ H[15])
    W[2] = (M32[0] ^ H[0]) + (M32[7] ^ H[7]) + (M32[9] ^ H[9]) - (M32[12] ^ H[12]) + (M32[15] ^ H[15])
    W[3] = (M32[0] ^ H[0]) - (M32[1] ^ H[1]) + (M32[8] ^ H[8]) - (M32[10] ^ H[10]) + (M32[13] ^ H[13])
    W[4] = (M32[1] ^ H[1]) + (M32[2] ^ H[2]) + (M32[9] ^ H[9]) - (M32[11] ^ H[11]) - (M32[14] ^ H[14])
    W[5] = (M32[3] ^ H[3]) - (M32[2] ^ H[2]) + (M32[10] ^ H[10]) - (M32[12] ^ H[12]) + (M32[15] ^ H[15])
    W[6] = (M32[4] ^ H[4]) - (M32[0] ^ H[0]) - (M32[3] ^ H[3]) - (M32[11] ^ H[11]) + (M32[13] ^ H[13])
    W[7] = (M32[1] ^ H[1]) - (M32[4] ^ H[4]) - (M32[5] ^ H[5]) - (M32[12] ^ H[12]) - (M32[14] ^ H[14])
    W[8] = (M32[2] ^ H[2]) - (M32[5] ^ H[5]) - (M32[6] ^ H[6]) + (M32[13] ^ H[13]) - (M32[15] ^ H[15])
    W[9] = (M32[0] ^ H[0]) - (M32[3] ^ H[3]) + (M32[6] ^ H[6]) - (M32[7] ^ H[7]) + (M32[14] ^ H[14])
    W[10] = (M32[8] ^ H[8]) - (M32[1] ^ H[1]) - (M32[4] ^ H[4]) - (M32[7] ^ H[7]) + (M32[15] ^ H[15])
    W[11] = (M32[8] ^ H[8]) - (M32[0] ^ H[0]) - (M32[2] ^ H[2]) - (M32[5] ^ H[5]) + (M32[9] ^ H[9])
    W[12] = (M32[1] ^ H[1]) + (M32[3] ^ H[3]) - (M32[6] ^ H[6]) - (M32[9] ^ H[9]) + (M32[10] ^ H[10])
    W[13] = (M32[2] ^ H[2]) + (M32[4] ^ H[4]) + (M32[7] ^ H[7]) + (M32[10] ^ H[10]) + (M32[11] ^ H[11])
    W[14] = (M32[3] ^ H[3]) - (M32[5] ^ H[5]) + (M32[8] ^ H[8]) - (M32[11] ^ H[11]) - (M32[12] ^ H[12])
    W[15] = (M32[12] ^ H[12]) - (M32[4] ^ H[4]) - (M32[6] ^ H[6]) - (M32[9] ^ H[9]) + (M32[13] ^ H[13])
    if (printing):
        [print(f'W{i} = ', hex(W[i])) for i in range(16)]
    # for i in range(16):
    #     print(sys.getsizeof(W[i]))

    # Diffuse the differences in every word in a bijective manner with s32_i, and then add the values of the previous double pipe.
    Q[0] = s32_0(W[0]) + H[1]
    Q[1] = s32_1(W[1]) + H[2]
    Q[2] = s32_2(W[2]) + H[3]
    Q[3] = s32_3(W[3]) + H[4]
    Q[4] = s32_4(W[4]) + H[5]
    Q[5] = s32_0(W[5]) + H[6]
    Q[6] = s32_1(W[6]) + H[7]
    Q[7] = s32_2(W[7]) + H[8]
    Q[8] = s32_3(W[8]) + H[9]
    Q[9] = s32_4(W[9]) + H[10]
    Q[10] = s32_0(W[10]) + H[11]
    Q[11] = s32_1(W[11]) + H[12]
    Q[12] = s32_2(W[12]) + H[13]
    Q[13] = s32_3(W[13]) + H[14]
    Q[14] = s32_4(W[14]) + H[15]
    Q[15] = s32_0(W[15]) + H[0]

    # print("--------------")
    # for i in range(16):
    #     print(sys.getsizeof(Q[i]))
    # Message expansion or f_1 in the documentation
    # It has 16 rounds
    # Blue Midnight Wish has two tunable security parameters
    # The parameters are named EXPAND_1_ROUNDS and EXPAND_2_ROUNDS
    # The following relation for these parameters should be satisfied:
    # EXPAND_1_ROUNDS + EXPAND_2_ROUNDS = 16

    for i in range(expand_1_rounds):
        Q[i + 16] = expand32_1(i + 16, M32, H, Q)

    for i in range(expand_1_rounds, expand_1_rounds + expand_2_rounds):
        Q[i + 16] = expand32_2(i + 16, M32, H, Q)
    if printing:
        [print(f'Q{i} = ', hex(Q[i])) for i in range(0, 32)]

    # Blue Midnight Wish has two temporary cumulative variables that accumulate via XORing
    # 16 new variables that are produced in the Message Expansion part
    XL32 = Q[16] ^ Q[17] ^ Q[18] ^ Q[19] ^ Q[20] ^ Q[21] ^ Q[22] ^ Q[23]
    XH32 = XL32 ^ Q[24] ^ Q[25] ^ Q[26] ^ Q[27] ^ Q[28] ^ Q[29] ^ Q[30] ^ Q[31]
    # This part is the function f_2 - in the documentation
    if printing:
        print('XL32: ', hex(XL32))
        print('XH32', hex(XH32))
    # Compute the double chaining pipe for the next message block.
    H[0] = (shl32(XH32, np.uint32(5)) ^ shr32(Q[16], np.uint32(5)) ^ M32[0]) + (XL32 ^ Q[24] ^ Q[0])
    H[1] = (shr32(XH32, np.uint32(7)) ^ shl32(Q[17], np.uint32(8)) ^ M32[1]) + (XL32 ^ Q[25] ^ Q[1])
    H[2] = (shr32(XH32, np.uint32(5)) ^ shl32(Q[18], np.uint32(5)) ^ M32[2]) + (XL32 ^ Q[26] ^ Q[2])
    H[3] = (shr32(XH32, np.uint32(1)) ^ shl32(Q[19], np.uint32(5)) ^ M32[3]) + (XL32 ^ Q[27] ^ Q[3])
    H[4] = (shr32(XH32, np.uint32(3)) ^ Q[20] ^ M32[4]) + (XL32 ^ Q[28] ^ Q[4])
    H[5] = (shl32(XH32, np.uint32(6)) ^ shr32(Q[21], np.uint32(6)) ^ M32[5]) + (XL32 ^ Q[29] ^ Q[5])
    H[6] = (shr32(XH32, np.uint32(4)) ^ shl32(Q[22], np.uint32(6)) ^ M32[6]) + (XL32 ^ Q[30] ^ Q[6])
    H[7] = (shr32(XH32, np.uint32(11)) ^ shl32(Q[23], np.uint32(2)) ^ M32[7]) + (XL32 ^ Q[31] ^ Q[7])

    H[8] = rotl32(H[4], np.uint32(9)) + (XH32 ^ Q[24] ^ M32[8]) + (shl32(XL32, np.uint32(8)) ^ Q[23] ^ Q[8])
    H[9] = rotl32(H[5], np.uint32(10)) + (XH32 ^ Q[25] ^ M32[9]) + (shr32(XL32, np.uint32(6)) ^ Q[16] ^ Q[9])
    H[10] = rotl32(H[6], np.uint32(11)) + (XH32 ^ Q[26] ^ M32[10]) + (shl32(XL32, np.uint32(6)) ^ Q[17] ^ Q[10])
    H[11] = rotl32(H[7], np.uint32(12)) + (XH32 ^ Q[27] ^ M32[11]) + (shl32(XL32, np.uint32(4)) ^ Q[18] ^ Q[11])
    H[12] = rotl32(H[0], np.uint32(13)) + (XH32 ^ Q[28] ^ M32[12]) + (shr32(XL32, np.uint32(3)) ^ Q[19] ^ Q[12])
    H[13] = rotl32(H[1], np.uint32(14)) + (XH32 ^ Q[29] ^ M32[13]) + (shr32(XL32, np.uint32(4)) ^ Q[20] ^ Q[13])
    H[14] = rotl32(H[2], np.uint32(15)) + (XH32 ^ Q[30] ^ M32[14]) + (shr32(XL32, np.uint32(7)) ^ Q[21] ^ Q[14])
    H[15] = rotl32(H[3], np.uint32(16)) + (XH32 ^ Q[31] ^ M32[15]) + (shr32(XL32, np.uint32(2)) ^ Q[22] ^ Q[15])
    if printing:
        [print(f'H{i} = ', hex(H[i])) for i in range(16)]

    return M32, H


def expand64_1(i, M64, H, Q):
    return (s64_1(Q[i - 16]) + s64_2(Q[i - 15]) + s64_3(Q[i - 14]) + s64_0(Q[i - 13])
            + s64_1(Q[i - 12]) + s64_2(Q[i - 11]) + s64_3(Q[i - 10]) + s64_0(Q[i - 9])
            + s64_1(Q[i - 8]) + s64_2(Q[i - 7]) + s64_3(Q[i - 6]) + s64_0(Q[i - 5])
            + s64_1(Q[i - 4]) + s64_2(Q[i - 3]) + s64_3(Q[i - 2]) + s64_0(Q[i - 1])
            + ((np.uint64(i) * np.uint64(0x0555555555555555) + rotl64(M64[np.uint64((i - 16) % 16)],
                                                                      (np.uint64((i - 16) % 16)) + np.uint64(1))
                + rotl64(M64[(i - 13) % 16], ((i - 13) % 16) + 1)
                - rotl64(M64[(i - 6) % 16], ((i - 6) % 16) + 1)) ^ H[(i - 16 + 7) % 16]))


# Message expansion function 2
def expand64_2(i, M64, H, Q):
    return (Q[i - 16] + r64_01(Q[i - 15]) + Q[i - 14] + r64_02(Q[i - 13])
            + Q[i - 12] + r64_03(Q[i - 11]) + Q[i - 10] + r64_04(Q[i - 9])
            + Q[i - 8] + r64_05(Q[i - 7]) + Q[i - 6] + r64_06(Q[i - 5])
            + Q[i - 4] + r64_07(Q[i - 3]) + s64_4(Q[i - 2]) + s64_5(Q[i - 1])
            + ((np.uint64(i) * np.uint64(0x0555555555555555) + rotl64(M64[np.uint64((i - 16) % 16)],
                                                                      np.uint64(((i - 16) % 16)) + np.uint64(1))
                + rotl64(M64[(i - 13) % 16], ((i - 13) % 16) + 1)
                - rotl64(M64[(i - 6) % 16], ((i - 6) % 16) + 1)) ^ H[(i - 16 + 7) % 16]))


def Compression512(M64, H):
    W = np.zeros(16, dtype=np.uint64)
    Q = np.zeros(32, dtype=np.uint64)
    if printing:
        [print(f'M{i} = ', hex(M64[i])) for i in range(16)]
    # This part is the function f0 - in the documentation
    # First we mix the message block *M64 (M in the documentation)
    # with the previous double pipe *P.
    # For a fixed previous double pipe, or fixed message block, this
    # part is bijection.
    # This transformation diffuses every one bit difference in 5 words.
    W[0] = (M64[5] ^ H[5]) - (M64[7] ^ H[7]) + (M64[10] ^ H[10]) + (M64[13] ^ H[13]) + (M64[14] ^ H[14])
    W[1] = (M64[6] ^ H[6]) - (M64[8] ^ H[8]) + (M64[11] ^ H[11]) + (M64[14] ^ H[14]) - (M64[15] ^ H[15])
    W[2] = (M64[0] ^ H[0]) + (M64[7] ^ H[7]) + (M64[9] ^ H[9]) - (M64[12] ^ H[12]) + (M64[15] ^ H[15])
    W[3] = (M64[0] ^ H[0]) - (M64[1] ^ H[1]) + (M64[8] ^ H[8]) - (M64[10] ^ H[10]) + (M64[13] ^ H[13])
    W[4] = (M64[1] ^ H[1]) + (M64[2] ^ H[2]) + (M64[9] ^ H[9]) - (M64[11] ^ H[11]) - (M64[14] ^ H[14])
    W[5] = (M64[3] ^ H[3]) - (M64[2] ^ H[2]) + (M64[10] ^ H[10]) - (M64[12] ^ H[12]) + (M64[15] ^ H[15])
    W[6] = (M64[4] ^ H[4]) - (M64[0] ^ H[0]) - (M64[3] ^ H[3]) - (M64[11] ^ H[11]) + (M64[13] ^ H[13])
    W[7] = (M64[1] ^ H[1]) - (M64[4] ^ H[4]) - (M64[5] ^ H[5]) - (M64[12] ^ H[12]) - (M64[14] ^ H[14])
    W[8] = (M64[2] ^ H[2]) - (M64[5] ^ H[5]) - (M64[6] ^ H[6]) + (M64[13] ^ H[13]) - (M64[15] ^ H[15])
    W[9] = (M64[0] ^ H[0]) - (M64[3] ^ H[3]) + (M64[6] ^ H[6]) - (M64[7] ^ H[7]) + (M64[14] ^ H[14])
    W[10] = (M64[8] ^ H[8]) - (M64[1] ^ H[1]) - (M64[4] ^ H[4]) - (M64[7] ^ H[7]) + (M64[15] ^ H[15])
    W[11] = (M64[8] ^ H[8]) - (M64[0] ^ H[0]) - (M64[2] ^ H[2]) - (M64[5] ^ H[5]) + (M64[9] ^ H[9])
    W[12] = (M64[1] ^ H[1]) + (M64[3] ^ H[3]) - (M64[6] ^ H[6]) - (M64[9] ^ H[9]) + (M64[10] ^ H[10])
    W[13] = (M64[2] ^ H[2]) + (M64[4] ^ H[4]) + (M64[7] ^ H[7]) + (M64[10] ^ H[10]) + (M64[11] ^ H[11])
    W[14] = (M64[3] ^ H[3]) - (M64[5] ^ H[5]) + (M64[8] ^ H[8]) - (M64[11] ^ H[11]) - (M64[12] ^ H[12])
    W[15] = (M64[12] ^ H[12]) - (M64[4] ^ H[4]) - (M64[6] ^ H[6]) - (M64[9] ^ H[9]) + (M64[13] ^ H[13])
    if printing:
        [print(f'W{i} = ', hex(W[i])) for i in range(16)]

    # Diffuse the differences in every word in a bijective manner with s64_i,
    # and then add the values of the previous double pipe.
    Q[0] = s64_0(W[0]) + H[1]
    Q[1] = s64_1(W[1]) + H[2]
    Q[2] = s64_2(W[2]) + H[3]
    Q[3] = s64_3(W[3]) + H[4]
    Q[4] = s64_4(W[4]) + H[5]
    Q[5] = s64_0(W[5]) + H[6]
    Q[6] = s64_1(W[6]) + H[7]
    Q[7] = s64_2(W[7]) + H[8]
    Q[8] = s64_3(W[8]) + H[9]
    Q[9] = s64_4(W[9]) + H[10]
    Q[10] = s64_0(W[10]) + H[11]
    Q[11] = s64_1(W[11]) + H[12]
    Q[12] = s64_2(W[12]) + H[13]
    Q[13] = s64_3(W[13]) + H[14]
    Q[14] = s64_4(W[14]) + H[15]
    Q[15] = s64_0(W[15]) + H[0]

    # This is the Message expansion or f_1 in the documentation.
    # It has 16 rounds.
    # Blue Midnight Wish has two tunable security parameters.
    # The parameters are named EXPAND_1_ROUNDS and EXPAND_2_ROUNDS.
    # The following relation for these parameters should be satisfied:
    # EXPAND_1_ROUNDS + EXPAND_2_ROUNDS = 16
    for i in range(expand_1_rounds):
        Q[i + 16] = expand64_1(i + 16, M64, H, Q)
    for i in range(expand_1_rounds, expand_1_rounds + expand_2_rounds):
        Q[i + 16] = expand64_2(i + 16, M64, H, Q)
    if printing:
        [print(f'Q{i} = ', hex(Q[i])) for i in range(0, 32)]

    # Blue Midnight Wish has two temporary cumulative variables that accumulate via XORing
    # 16 new variables that are produced in the Message Expansion part.
    XL64 = Q[16] ^ Q[17] ^ Q[18] ^ Q[19] ^ Q[20] ^ Q[21] ^ Q[22] ^ Q[23]
    XH64 = XL64 ^ Q[24] ^ Q[25] ^ Q[26] ^ Q[27] ^ Q[28] ^ Q[29] ^ Q[30] ^ Q[31]
    if printing:
        print('XL64: ', hex(XL64))
        print('XH64', hex(XH64))
    # This part is the function f_2 - in the documentation

    # Compute the double chaining pipe for the next message block.
    H[0] = (shl64(XH64, np.uint64(5)) ^ shr64(Q[16], np.uint64(5)) ^ M64[0]) + (XL64 ^ Q[24] ^ Q[0])
    H[1] = (shr64(XH64, np.uint64(7)) ^ shl64(Q[17], np.uint64(8)) ^ M64[1]) + (XL64 ^ Q[25] ^ Q[1])
    H[2] = (shr64(XH64, np.uint64(5)) ^ shl64(Q[18], np.uint64(5)) ^ M64[2]) + (XL64 ^ Q[26] ^ Q[2])
    H[3] = (shr64(XH64, np.uint64(1)) ^ shl64(Q[19], np.uint64(5)) ^ M64[3]) + (XL64 ^ Q[27] ^ Q[3])
    H[4] = (shr64(XH64, np.uint64(3)) ^ Q[20] ^ M64[4]) + (XL64 ^ Q[28] ^ Q[4])
    H[5] = (shl64(XH64, np.uint64(6)) ^ shr64(Q[21], np.uint64(6)) ^ M64[5]) + (XL64 ^ Q[29] ^ Q[5])
    H[6] = (shr64(XH64, np.uint64(4)) ^ shl64(Q[22], np.uint64(6)) ^ M64[6]) + (XL64 ^ Q[30] ^ Q[6])
    H[7] = (shr64(XH64, np.uint64(11)) ^ shl64(Q[23], np.uint64(2)) ^ M64[7]) + (XL64 ^ Q[31] ^ Q[7])
    H[8] = rotl64(H[4], np.uint64(9)) + (XH64 ^ Q[24] ^ M64[8]) + (shl64(XL64, np.uint64(8)) ^ Q[23] ^ Q[8])
    H[9] = rotl64(H[5], np.uint64(10)) + (XH64 ^ Q[25] ^ M64[9]) + (shr64(XL64, np.uint64(6)) ^ Q[16] ^ Q[9])
    H[10] = rotl64(H[6], np.uint64(11)) + (XH64 ^ Q[26] ^ M64[10]) + (shl64(XL64, np.uint64(6)) ^ Q[17] ^ Q[10])
    H[11] = rotl64(H[7], np.uint64(12)) + (XH64 ^ Q[27] ^ M64[11]) + (shl64(XL64, np.uint64(4)) ^ Q[18] ^ Q[11])
    H[12] = rotl64(H[0], np.uint64(13)) + (XH64 ^ Q[28] ^ M64[12]) + (shr64(XL64, np.uint64(3)) ^ Q[19] ^ Q[12])
    H[13] = rotl64(H[1], np.uint64(14)) + (XH64 ^ Q[29] ^ M64[13]) + (shr64(XL64, np.uint64(4)) ^ Q[20] ^ Q[13])
    H[14] = rotl64(H[2], np.uint64(15)) + (XH64 ^ Q[30] ^ M64[14]) + (shr64(XL64, np.uint64(7)) ^ Q[21] ^ Q[14])
    H[15] = rotl64(H[3], np.uint64(16)) + (XH64 ^ Q[31] ^ M64[15]) + (shr64(XL64, np.uint64(2)) ^ Q[22] ^ Q[15])
    if printing:
        [print(f'H{i} = ', hex(H[i])) for i in range(16)]

    return M64, H
