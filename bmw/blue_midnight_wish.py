from components import i224p2, i256p2, i384p2, i512p2, const32final, const64final
import warnings
import numpy as np
from functions import compression256, compression512

warnings.filterwarnings("ignore")


def pad_32(message: bytearray) -> bytearray:
    m_length = len(message) * 8
    # if m_length % 512 != 0:
    message.append(0x80)
    for i in range(512):
        if (len(message) * 8) % 512 == 448:
            break
        message.append(0)
    message += m_length.to_bytes(8, byteorder='little')
    if len(message) % 64 != 0:
        raise AssertionError("Padding went wrong. Try again. Error in pad_32()")
    return message


def pad_64(message: bytearray) -> bytearray:
    m_length = len(message) * 8
    # if m_length % 512 != 0:
    message.append(0x80)
    for i in range(1024):
        if (len(message) * 8) % 1024 == 960:
            break
        message.append(0)
    message += m_length.to_bytes(8, byteorder='little')
    if len(message) % 128 != 0:
        raise AssertionError("Padding went wrong. Try again. Error in pad_64()")
    return message


def divide_message(message: bytearray, hashBitLength: int) -> np.array:
    match hashBitLength:
        case 224 | 256:
            divided_message = np.zeros(0, dtype=np.uint32)
            for i in range(len(message) // 64):
                for j in range(0, 64, 4):
                    divided_message = np.append(divided_message,
                                                int.from_bytes(message[(j + 64 * i):(j + 64 * i) + 4],
                                                               byteorder='little'))
            return np.array(divided_message, dtype=np.uint32)
        case 384 | 512:
            divided_message = np.zeros(0, dtype=np.uint64)
            for i in range(len(message) // 128):
                for j in range(0, 128, 8):
                    divided_message = np.append(divided_message,
                                                np.uint64(int.from_bytes(message[(j + 128 * i):(j + 128 * i) + 8],
                                                                         byteorder='little')))
            return np.array(divided_message, dtype=np.uint64)
        case _:
            raise AssertionError('Incorrect Hash bit length. Error in divide_message()')


def pipe_init(hashBitLengh):
    match hashBitLengh:
        case 224:
            pipe = np.array(i224p2, dtype=np.uint32)
        case 256:
            pipe = np.array(i256p2, dtype=np.uint32)
        case 384:
            pipe = np.array(i384p2, dtype=np.uint64)
        case 512:
            pipe = np.array(i512p2, dtype=np.uint64)
        case _:
            raise AssertionError('Something went wrong while initializing the Double Pipe. Error in pipe_init()')
    return pipe


def update(divided_message, pipe, hashBitLengh):
    match hashBitLengh:
        case 224 | 256:
            divided_message, new_pipe = compression256(divided_message, pipe)
        case 384 | 512:
            divided_message, new_pipe = compression512(divided_message, pipe)
        case _:
            raise AssertionError('Incorrect Hash bit length. Error in update()')

    return divided_message, new_pipe


def final(pipe, hashBitLengh):
    match hashBitLengh:
        case 224 | 256:
            const32final_np = np.array(const32final, dtype=np.uint32)
            old_pipe, hashed_pipe = compression256(pipe, const32final_np)
        case 384 | 512:
            const64final_np = np.array(const64final, dtype=np.uint64)
            old_pipe, hashed_pipe = compression512(pipe, const64final_np)
        case _:
            raise AssertionError("Final shuffle failed. Error at final()")
    return old_pipe, hashed_pipe


def print_message(message, divided_message, pipe):
    print('Bytes message: ', message)
    print('Divided message into numpy array', divided_message)
    print('Double pipe: ', pipe)


def get_hash(hashed_pipe: np.array, hashBitLengh: int):
    bytes_hash = hashed_pipe.tobytes()
    hash = ''
    match hashBitLengh:
        case 224:
            for i in range(36, 64):
                hash += format(bytes_hash[i], '02x')
        case 256:
            for i in range(32, 64):
                hash += format(bytes_hash[i], '02x')
        case 384:
            for i in range(80, 128):
                hash += format(bytes_hash[i], '02x')
        case 512:
            for i in range(64, 128):
                hash += (format(bytes_hash[i], '02x'))
        case _:
            raise AssertionError('Printing Hash failed \n')

    return hash


def bmw(message, hashBitLength):
    message = bytearray(message)
    match hashBitLength:
        case 224 | 256:
            padded_message = pad_32(message)
            divider = 64
        case 384 | 512:
            padded_message = pad_64(message)
            divider = 128
        case _:
            raise AssertionError('Incorrect Hash bit length. Error in bmw()')

    pipe = pipe_init(hashBitLength)
    for i in range(len(padded_message) // divider):
        divided_message = divide_message(padded_message[i * divider:(i + 1) * divider], hashBitLength)
        _, pipe = update(divided_message, pipe, hashBitLength)
    new_pipe, hashed_pipe = final(pipe, hashBitLength)
    return get_hash(hashed_pipe, hashBitLength)
