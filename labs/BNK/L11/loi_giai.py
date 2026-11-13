truong = {3: "000000", 4: "000000250000", 11: "000042", 39: "00"}
bit = 0
for so in truong:
    bit |= 1 << (64 - so)
print("%016X" % bit)
print(len("0210" + "%016X" % bit + "".join(truong[k] for k in sorted(truong))))
