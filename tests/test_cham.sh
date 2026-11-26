#!/usr/bin/env bash
# Kiểm đơn vị cho labs/cham.sh v2 (WP-0.12): 6 ngôn ngữ, ca ẩn, chống hardcode, sai số số thực, bài giấy, dự án Python unittest.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
F="$ROOT/tests/fixtures/labs"
CHAM="$ROOT/labs/cham.sh"

pass=0
fail=0
ok() { pass=$((pass + 1)); echo "[PASS] $1"; }
bad() { fail=$((fail + 1)); echo "[FAIL] $1"; }

for lang in py_ca py_ham c_ok java_ok sql_ok sql_seed sh_ok js_ok float_ok giay_ok; do
    if bash "$CHAM" "$F/$lang" >/dev/null 2>&1; then
        ok "$lang loi_giai"
    else
        bad "$lang loi_giai"
    fi
done

# Chống hardcode: sai_gia.py qua ca công khai nhưng phải FAIL ca_an/
if bash "$CHAM" "$F/py_ca" "$F/py_ca/sai_gia.py" >/dev/null 2>&1; then
    bad "py_ca sai_gia khong bi chan o ca_an"
else
    ok "py_ca sai_gia bi chan o ca_an"
fi
if bash "$CHAM" "$F/py_ham" "$F/py_ham/sai_gia.py" >/dev/null 2>&1; then
    bad "py_ham sai_gia khong bi chan o ham.json"
else
    ok "py_ham sai_gia bi chan o ham.json"
fi

# Sai số vượt ngưỡng phải FAIL
if bash "$CHAM" "$F/float_ok" "$F/float_ok/loi_sai.py" >/dev/null 2>&1; then
    bad "float_ok loi_sai khong bi chan"
else
    ok "float_ok loi_sai bi chan"
fi

# Bài giấy thiếu mục phải FAIL
if bash "$CHAM" "$F/giay_ok" "$F/giay_ok/loi_sai.md" >/dev/null 2>&1; then
    bad "giay_ok loi_sai khong bi chan"
else
    ok "giay_ok loi_sai bi chan"
fi

# Dự án du_an (unittest): đúng PASS, sai FAIL
if bash "$CHAM" "$F/du_an_py" --du-an "$F/du_an_py/loi_giai" >/dev/null 2>&1; then
    ok "du_an_py loi_giai"
else
    bad "du_an_py loi_giai"
fi

if bash "$CHAM" "$F/du_an_py" --du-an "$F/du_an_py/loi_sai" >/dev/null 2>&1; then
    bad "du_an_py loi_sai khong bi chan"
else
    ok "du_an_py loi_sai bi chan"
fi

echo "test_cham: $pass PASS, $fail FAIL"
[ "$fail" -eq 0 ]
