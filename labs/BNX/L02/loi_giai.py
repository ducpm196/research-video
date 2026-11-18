def varint(n):
    out = []
    while True:
        b, n = n & 0x7F, n >> 7
        out.append(b | 0x80 if n else b)
        if n == 0:
            return bytes(out)


def field(num, wire, payload):
    return varint(num << 3 | wire) + payload


m = field(1, 0, varint(20))
m += field(6, 0, varint(70000))
m += field(7, 2, varint(5) + b"ATM01")
print(m.hex(" "))
print(len(m), "byte")
