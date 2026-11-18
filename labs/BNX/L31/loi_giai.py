import json
NK = [
    '{"t":500,"dv":"gw","cid":"c9","ev":"nhan"}',
    '{"t":505,"dv":"gw","cid":"d4","ev":"nhan"}',
    '{"t":520,"dv":"pay","cid":"c9","ev":"tru"}',
    '{"t":526,"dv":"pay","cid":"d4","ev":"loi"}',
    '{"t":560,"dv":"gw","cid":"c9","ev":"tra"}',
    '{"t":545,"dv":"led","cid":"c9","ev":"ghi"}',
]
SU_KIEN = [json.loads(d) for d in NK]
c9 = sorted((d for d in SU_KIEN if d["cid"] == "c9"), key=lambda d: d["t"])
print("c9:", " > ".join(d["dv"] + ":" + d["ev"] for d in c9))
print("c9 mat", c9[-1]["t"] - c9[0]["t"], "ms")
loi = sum(1 for d in SU_KIEN if d["ev"] == "loi")
print("so dong loi:", loi)
YEU_CAU, YEU_CAU_LOI, SLO = 200, 6, 0.99
print("toc do dot:", round(YEU_CAU_LOI / YEU_CAU / (1 - SLO), 1))
