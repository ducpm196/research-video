import zlib
khoa = "session::s77"
r = (zlib.crc32(khoa.encode()) >> 16) & 0x7FFF
print("thung ao (1024):", r % 1024, "| (128):", r % 128)
doc, cas = 300, 4
def ghi(moi, cas_kem):
    global doc, cas
    if cas_kem != cas:
        return "tu choi"
    doc, cas = moi, cas + 1
    return "ghi duoc, CAS moi = %d" % cas
d1, c1 = doc, cas
d2, c2 = doc, cas
print("P1:", ghi(d1 + 20, c1))
print("P2:", ghi(d2 - 50, c2))
d2, c2 = doc, cas
print("P2 lan 2:", ghi(d2 - 50, c2))
print("cuoi:", doc, cas)
