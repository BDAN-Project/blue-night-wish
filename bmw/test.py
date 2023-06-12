from colorama import Fore
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
            hash_to_compare = bmw(int.to_bytes(message,int(msg_length/8), byteorder='big'), n).upper()
            print(Fore.WHITE + "\n===============================\n",)
            print( "MSG: ", message)
            print("Len: ", int(msg_length/8))
            print("Expected: ", hash)
            if hash == hash_to_compare:
                print(Fore.GREEN + "Hash:",hash_to_compare)
            else:
                print(Fore.RED + "Hash:",hash_to_compare)

BMW_test(224, "tests/ShortMsgKAT_224.txt")
BMW_test(256, "tests/ShortMsgKAT_256.txt")
BMW_test(384, "tests/ShortMsgKAT_384.txt")
BMW_test(512, "tests/ShortMsgKAT_512.txt")

BMW_test(224, "tests/LongMsgKAT_224.txt")
BMW_test(256, "tests/LongMsgKAT_256.txt")
BMW_test(384, "tests/LongMsgKAT_384.txt")
BMW_test(512, "tests/LongMsgKAT_512.txt")