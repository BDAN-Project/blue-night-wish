import pytest
from blue_midnight_wish import bmw

def BMW_test(n, filePath):
    length = []
    msg = []
    md = []
    with open(filePath, "r") as opened_file:
        for line in opened_file:
            if line[0] == 'L':
                length.append(int(line[6:].rstrip()))
            elif line[0] == 'M' and line[1] == 's' :
                msg.append(int(line[6:].rstrip(),16))
            elif line[0] == 'M' and line[1] == 'D' :
                md.append(line[5:].rstrip())
    for msg_length,message,hash in zip(length,msg,md):
         if msg_length % 8 == 0:
            assert hash == bmw(int.to_bytes(message,int(msg_length/8), byteorder='big'), n).upper()

def test__short_message_BMW224():
    BMW_test(224, "tests/ShortMsgKAT_224.txt")

def test__short_message_BMW256():
    BMW_test(256, "tests/ShortMsgKAT_256.txt")

def test_short_message_BMW384():
    BMW_test(384, "tests/ShortMsgKAT_384.txt")

def test_short_message_BMW512():
    BMW_test(512, "tests/ShortMsgKAT_512.txt")

def test_long_message_BMW224():
    BMW_test(224, "tests/LongMsgKAT_224.txt")

def test__long_message_BMW256():
    BMW_test(256, "tests/LongMsgKAT_256.txt")

def test_long_message_BMW384():
    BMW_test(384, "tests/LongMsgKAT_384.txt")

def test_long_message_BMW512():
    BMW_test(512, "tests/LongMsgKAT_512.txt")