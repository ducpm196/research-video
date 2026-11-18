KHO = {"content": {"bank": {"en": {
    "the": {"sling:resourceType": "bank/components/card"},
    "vay": {"sling:resourceType": "bank/components/loan"}}}}}
TEP = ["/apps/bank/components/card/card.html",
       "/apps/bank/components/card/print.html",
       "/libs/bank/components/loan/loan.html"]
def nut(duong):
    n = KHO
    for ten in duong.strip("/").split("/"):
        n = n.get(ten) if isinstance(n, dict) else None
    return n
def xu_ly(url):
    duong, _, phan = url.partition(".")
    khuc = phan.split(".")
    chon = khuc[0] if len(khuc) > 1 else None
    n = nut(duong)
    if n is None:
        return "KHONG CO TAI NGUYEN"
    kieu = n["sling:resourceType"]
    for ten in ([chon] if chon else []) + [kieu.split("/")[-1]]:
        for goc in ("/apps/", "/libs/"):
            tep = goc + kieu + "/" + ten + ".html"
            if tep in TEP:
                return tep
    return "KHONG CO TEP DUNG"
for url in ["/content/bank/en/the.html", "/content/bank/en/the.print.html",
            "/content/bank/en/vay.html", "/content/bank/en/vay.print.html",
            "/content/bank/en/thieu.html"]:
    print(url.split("/")[-1], "->", xu_ly(url))
