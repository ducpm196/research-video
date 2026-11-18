def kiem(ma, duong):
    if ma is None:
        return 401
    if not ma["chu_ky_dung"] or ma["het_han"]:
        return 401
    if duong == "/chuyen-tien" and "chuyen_tien" not in ma["quyen"]:
        return 403
    return 200


an = {"chu_ky_dung": True, "het_han": False, "quyen": ["so_du"]}
binh = dict(an, quyen=["so_du", "chuyen_tien"])
gia = dict(binh, chu_ky_dung=False)
cu = dict(binh, het_han=True)
ca = [(None, "/so-du"), (gia, "/so-du"), (cu, "/chuyen-tien"),
      (an, "/so-du"), (an, "/chuyen-tien"), (binh, "/chuyen-tien")]
for i, (ma, duong) in enumerate(ca, 1):
    print(f"ca {i}: {kiem(ma, duong)}")

ban = {"b1": True, "b2": False, "b3": True, "b4": True}
khoe = [t for t, ok in ban.items() if ok]
dem = {t: 0 for t in khoe}
for i in range(250):
    dem[khoe[i % len(khoe)]] += 1
print(" ".join(f"{t}={n}" for t, n in dem.items()))
