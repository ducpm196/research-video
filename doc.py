import json
d = json.load(open("don.json"))
hang = d["hang"]
tong = sum(h["sl"] * h["gia"] for h in hang)
print(len(hang), tong)
