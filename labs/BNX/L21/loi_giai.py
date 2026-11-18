import hashlib
thu, dang, moi = 14_000_000, 3_000_000, 3_000_000
dti = (dang + moi) * 100 / thu
diem = (35 if thu >= 15_000_000 else 20) + 25 + 20
kq = "TU_CHOI" if (dang + moi) * 100 > 50 * thu or diem < 70 else "DUYET"
hd = "Hop dong vay 14000000 dong, ky han 24 thang\n"
sua = hd.replace("24", "25")
a = hashlib.sha256(hd.encode()).hexdigest()
b = hashlib.sha256(sua.encode()).hexdigest()
print(f"DTI: {dti:.1f} %")
print("Diem:", diem)
print("Quyet dinh:", kq)
print("Ma bam goc:", a[:12])
print("Vi tri khac:", sum(x != y for x, y in zip(a, b)))
