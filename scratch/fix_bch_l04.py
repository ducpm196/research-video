from pathlib import Path

p = Path("lessons/bch/L04_dong_chua_tieu.yaml")
t = p.read_text(encoding="utf-8")
t = t.replace("  - clear: true\n    show: |", "  - show: |")
old_chk1 = '  - show: |\n      <table class="t"><tr><th>đếm lại tổng tiền</th>'
new_chk1 = '  - clear: true\n    show: |\n      <table class="t"><tr><th>đếm lại tổng tiền</th>'
assert t.count(old_chk1) == 1
t = t.replace(old_chk1, new_chk1, 1)
p.write_text(t, encoding="utf-8")
print("Restored incremental steps + check#1 clear:true in BCH L04!")
