cat > don.json <<'EOF'
{
  "ma": 21,
  "khach": "Tran Mai",
  "hang": [
    {"ten": "ao", "sl": 4, "gia": 90000},
    {"ten": "non", "sl": 1, "gia": 45000},
    {"ten": "tat", "sl": 6, "gia": 8000}
  ],
  "da_tra": false
}
EOF
cat > doc.py <<'EOF'
import json
d = json.load(open("don.json"))
hang = d["hang"]
tong = sum(h["sl"] * h["gia"] for h in hang)
print(len(hang), tong)
EOF
python doc.py
echo 8080
echo 2
echo 13512
echo 3
