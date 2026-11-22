def crc_rem(bits, gen='1011'):
    b = list(bits)
    for i in range(len(bits) - len(gen) + 1):
        if b[i] == '1':
            for j in range(len(gen)): b[i+j] = '1' if b[i+j] != gen[j] else '0'
    return ''.join(b[-(len(gen)-1):])
d = '11010011101100'; r = crc_rem(d + '000'); tx = d + r
print(f'crc_rem={r}')
print(f'tx_frame_len={len(tx)}')
print(f'rx_ok={int(crc_rem(tx) == "000")}')
