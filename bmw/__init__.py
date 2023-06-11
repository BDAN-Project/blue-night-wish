from blue_midnight_wish import bmw


def main():
    # hash(int.to_bytes(0x80, 4), 256)
    # bmw(b'abc', 224)
    # bmw(b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq', 224)
    # bmw(b'abc', 256)
    # bmw(b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq', 256)
    # bmw(b'abc', 384)
    # bmw(b'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnmnopqrsmopqrstu', 384)
    # bmw(b'abc', 512)
    # bmw(b'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnmnopqrsmopqrstu', 512)
    # 6CF1F720CC1A79EB0A5462BF13EFD47499CA52179C6F575147217577
    bmw(int.to_bytes(0x0, 0, byteorder='big'), 224)
    bmw(int.to_bytes(0x724627916C50338643E6996F07877EAFD96BDF01DA7E991D4155B9BE1295EA7D21C9391F4C4A41C75F77E5D27389253393725F1427F57914B273AB862B9E31DABCE506E558720520D33352D119F699E784F9E548FF91BC35CA147042128709820D69A8287EA3257857615EB0321270E94B84F446942765CE882B191FAEE7E1C87E0F0BD4E0CD8A927703524B559B769CA4ECE1F6DBF313FDCF67C572EC4185C1A88E86EC11B6454B371980020F19633B6B95BD280E4FBCB0161E1A82470320CEC6ECFA25AC73D09F1536F286D3F9DACAFB2CD1D0CE72D64D197F5C7520B3CCB2FD74EB72664BA93853EF41EABF52F015DD591500D018DD162815CC993595B195
, 256, byteorder='big'), 256)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(e)
