import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
d, gen = kv['data'], kv['gen']; k = len(gen) - 1
def crc_rem(bits):
    b = list(bits)
    for i in range(len(bits) - k):
        if b[i] == '1':
            for j in range(len(gen)): b[i+j] = '1' if b[i+j] != gen[j] else '0'
    return ''.join(b[-k:])
r = crc_rem(d + '0'*k); tx = d + r
print(f'crc_rem={r}')
print(f'tx_frame_len={len(tx)}')
print(f'rx_ok={int(crc_rem(tx) == "0"*k)}')
