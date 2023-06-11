import numpy as np


def rotl32(x: np.uint32, n: np.uint32) -> np.uint32:
    x = np.uint32(x)
    n = np.uint32(n)
    return (x << n) | (x >> (32 - n))


def rotr32(x: np.uint32, n: np.uint32) -> np.uint32:
    x = np.uint32(x)
    n = np.uint32(n)
    return (x >> n) | (x << (32 - n))


def rotl64(x: np.uint64, n: np.uint64) -> np.uint64:
    x = np.uint64(x)
    n = np.uint64(n)
    return (x << n) | (x >> np.uint64((64 - n)))


def rotr64(x: np.uint64, n: np.uint64) -> np.uint64:
    x = np.uint64(x)
    n = np.uint64(n)
    return (x >> n) | (x << np.uint64((64 - n)))


def shl32(x: np.uint32, n: np.uint32) -> np.uint32:
    x = np.uint32(x)
    n = np.uint32(n)
    return x << n


def shr32(x: np.uint32, n: np.uint32) -> np.uint32:
    x = np.uint32(x)
    n = np.uint32(n)
    return x >> n


def shl64(x: np.uint64, n: np.uint64) -> np.uint64:
    x = np.uint64(x)
    n = np.uint64(n)
    return x << n


def shr64(x: np.uint64, n: np.uint64) -> np.uint64:
    x = np.uint64(x)
    n = np.uint64(n)
    return x >> n


# BlueMidnightWish224 initial double chaining pipe
i224p2 = np.array([
    0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f,
    0x10111213, 0x14151617, 0x18191a1b, 0x1c1d1e1f,
    0x20212223, 0x24252627, 0x28292a2b, 0x2c2d2e2f,
    0x30313233, 0x34353637, 0x38393a3b, 0x3c3d3e3f
], dtype=np.uint32)

# BlueMidnightWish256 initial double chaining pipe
i256p2 = np.array([
    0x40414243, 0x44454647,
    0x48494a4b, 0x4c4d4e4f,
    0x50515253, 0x54555657,
    0x58595a5b, 0x5c5d5e5f,
    0x60616263, 0x64656667,
    0x68696a6b, 0x6c6d6e6f,
    0x70717273, 0x74757677,
    0x78797a7b, 0x7c7d7e7f
], dtype=np.uint32)

# BlueMidnightWish384 initial double chaining pipe
i384p2 = np.array([
    0x0001020304050607, 0x08090a0b0c0d0e0f,
    0x1011121314151617, 0x18191a1b1c1d1e1f,
    0x2021222324252627, 0x28292a2b2c2d2e2f,
    0x3031323334353637, 0x38393a3b3c3d3e3f,
    0x4041424344454647, 0x48494a4b4c4d4e4f,
    0x5051525354555657, 0x58595a5b5c5d5e5f,
    0x6061626364656667, 0x68696a6b6c6d6e6f,
    0x7071727374757677, 0x78797a7b7c7d7e7f
], dtype=np.uint64)
# BlueMidnightWish512 initial double chaining pipe
i512p2 = np.array([
    0x8081828384858687, 0x88898a8b8c8d8e8f,
    0x9091929394959697, 0x98999a9b9c9d9e9f,
    0xa0a1a2a3a4a5a6a7, 0xa8a9aaabacadaeaf,
    0xb0b1b2b3b4b5b6b7, 0xb8b9babbbcbdbebf,
    0xc0c1c2c3c4c5c6c7, 0xc8c9cacbcccdcecf,
    0xd0d1d2d3d4d5d6d7, 0xd8d9dadbdcdddedf,
    0xe0e1e2e3e4e5e6e7, 0xe8e9eaebecedeeef,
    0xf0f1f2f3f4f5f6f7, 0xf8f9fafbfcfdfeff
], dtype=np.uint64)

const32final = np.array([
    0xaaaaaaa0, 0xaaaaaaa1, 0xaaaaaaa2, 0xaaaaaaa3,
    0xaaaaaaa4, 0xaaaaaaa5, 0xaaaaaaa6, 0xaaaaaaa7,
    0xaaaaaaa8, 0xaaaaaaa9, 0xaaaaaaaa, 0xaaaaaaab,
    0xaaaaaaac, 0xaaaaaaad, 0xaaaaaaae, 0xaaaaaaaf
], dtype=np.uint32)
const64final = np.array([
    0xaaaaaaaaaaaaaaa0, 0xaaaaaaaaaaaaaaa1,
    0xaaaaaaaaaaaaaaa2, 0xaaaaaaaaaaaaaaa3,
    0xaaaaaaaaaaaaaaa4, 0xaaaaaaaaaaaaaaa5,
    0xaaaaaaaaaaaaaaa6, 0xaaaaaaaaaaaaaaa7,
    0xaaaaaaaaaaaaaaa8, 0xaaaaaaaaaaaaaaa9,
    0xaaaaaaaaaaaaaaaa, 0xaaaaaaaaaaaaaaab,
    0xaaaaaaaaaaaaaaac, 0xaaaaaaaaaaaaaaad,
    0xaaaaaaaaaaaaaaae, 0xaaaaaaaaaaaaaaaf
], dtype=np.uint64)

blue_midnight_wish224_digest_size = 28
blue_midnight_wish224_block_size = 64
blue_midnight_wish256_digest_size = 32
blue_midnight_wish256_block_size = 64
blue_midnight_wish384_digest_size = 48
blue_midnight_wish384_block_size = 128
blue_midnight_wish512_digest_size = 64
blue_midnight_wish512_block_size = 128

expand_1_rounds = 2
expand_2_rounds = 14


# Components used for 224 and 256 bit version */
def s32_0(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return shr32(x, np.uint32(1)) ^ shl32(x, np.uint32(3)) ^ rotl32(x, np.uint32(4)) ^ rotl32(x, np.uint32(19))


def s32_1(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return shr32(x, np.uint32(1)) ^ shl32(x, np.uint32(2)) ^ rotl32(x, np.uint32(8)) ^ rotl32(x, np.uint32(23))


def s32_2(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return shr32(x, np.uint32(2)) ^ shl32(x, np.uint32(1)) ^ rotl32(x, np.uint32(12)) ^ rotl32(x, np.uint32(25))


def s32_3(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return shr32(x, np.uint32(2)) ^ shl32(x, np.uint32(2)) ^ rotl32(x, np.uint32(15)) ^ rotl32(x, np.uint32(29))


def s32_4(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return shr32(x, np.uint32(1)) ^ x


def s32_5(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return shr32(x, np.uint32(2)) ^ x


def r32_01(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return rotl32(x, np.uint32(3))


def r32_02(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return rotl32(x, np.uint32(7))


def r32_03(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return rotl32(x, np.uint32(13))


def r32_04(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return rotl32(x, np.uint32(16))


def r32_05(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return rotl32(x, np.uint32(19))


def r32_06(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return rotl32(x, np.uint32(23))


def r32_07(x: np.uint32) -> np.uint32:
    x = np.uint32(x)
    return rotl32(x, np.uint32(27))


# Components used for 384 and 512-bit version
def s64_0(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return (x >> np.uint64(1)) ^ (x << np.uint64(3)) ^ rotl64(x, np.uint64(4)) ^ rotl64(x, np.uint64(37))


def s64_1(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return (x >> np.uint64(1)) ^ (x << np.uint64(2)) ^ rotl64(x, np.uint64(13)) ^ rotl64(x, np.uint64(43))


def s64_2(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return (x >> np.uint64(2)) ^ (x << np.uint64(1)) ^ rotl64(x, np.uint64(19)) ^ rotl64(x, np.uint64(53))


def s64_3(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return (x >> np.uint64(2)) ^ (x << np.uint64(2)) ^ rotl64(x, np.uint64(28)) ^ rotl64(x, np.uint64(59))


def s64_4(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return (x >> np.uint64(1)) ^ x


def s64_5(x: np.uint64) -> np.uint64:
    return (x >> np.uint64(2)) ^ x


def r64_01(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return rotl64(x, np.uint64(5))


def r64_02(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return rotl64(x, np.uint64(11))


def r64_03(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return rotl64(x, np.uint64(27))


def r64_04(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return rotl64(x, np.uint64(32))


def r64_05(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return rotl64(x, np.uint64(37))


def r64_06(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return rotl64(x, np.uint64(43))


def r64_07(x: np.uint64) -> np.uint64:
    x = np.uint64(x)
    return rotl64(x, np.uint64(53))
