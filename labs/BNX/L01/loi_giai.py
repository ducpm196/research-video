import re

THE = re.compile(r"^[0-9]{16}$")


def kiem(req):
    loi = []
    v = req.get("soThe")
    if v is None:
        loi.append("soThe: thieu")
    elif not (type(v) is str and THE.fullmatch(v)):
        loi.append("soThe: sai dang")
    t = req.get("soTien")
    if t is None:
        loi.append("soTien: thieu")
    elif not (type(t) is int and t >= 50000):
        loi.append("soTien: phai la so nguyen >= 50000")
    return loi


thu = [
    {"soThe": "1234567890123456", "soTien": 200000},
    {"soThe": "123456", "soTien": 200000},
    {"soThe": "1234567890123456", "soTien": 20000},
    {"soThe": "1234567890123456", "soTien": "200000"},
    {"soTien": 200000},
]
for i, req in enumerate(thu, 1):
    loi = kiem(req)
    print(i, 400 if loi else 201, "; ".join(loi) or "-")
