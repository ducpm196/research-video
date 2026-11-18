truong = {"DEBIT.ACCT.NO": "5550001111", "CREDIT.ACCT.NO": "6660002222", "DEBIT.AMOUNT": "1250000"}
kv = ",".join(k + "=" + v for k, v in truong.items())
tin = ",".join(["FUNDS.TRANSFER", "ACTR/I/PROCESS", "INPUTTER/******/VN0010002", "", kv])
dau, cap = tin.split(",,")
print("ofs dau:", dau + ",,")
print("ofs cap:", cap)
print("so truong:", len(tin.split(",")[4:]))

cho = {"a1": "2tr", "a2": "1tr", "a3": "7tr"}
for cid, kq in [("a3", "OK"), ("a1", "OK"), ("a2", "LOI")]:
    print(cid, cho.pop(cid), "->", kq)
print("con cho:", len(cho))

tai, ms = 2000, 45
print("dang cho:", tai * ms // 1000)
moi_ket_noi = 1000 // ms
print("ket noi tuan tu:", -(-tai // moi_ket_noi))
