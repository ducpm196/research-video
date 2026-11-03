#!/usr/bin/env bash
# Quét bố cục bằng `lv.py render` riêng (không TTS, ~20 s/bài) cho các khoá cho trước; chỉ in bài có vấn đề.
# Lint không thấy tràn khung / chữ đè / chữ tràn mép hình — chỉ render đo được (pedagogy.md luật 24 bước 6).
# Lưu ý: ghi đè out/<KHOÁ>/<id>/frames — đừng chạy cho khoá đang có trong hàng đợi dựng.
# Chạy: bash audit/review/render_scan.sh aif llm swf …   → audit/review/render_scan.tsv (khoá, bài, vấn đề)
cd "$(dirname "$0")/../.." || exit 1
out=audit/review/render_scan.tsv
for c in "$@"; do
  for f in lessons/$c/L*_*.yaml; do
    r=$(PYTHONIOENCODING=utf-8 .venv/Scripts/python tools/lv.py render "$f" 2>&1)
    n=$(printf '%s\n' "$r" | grep -o '([0-9]* vấn đề)' | tail -1)
    if [ "$n" != "(0 vấn đề)" ]; then
      printf '%s\t%s\t%s\n' "$c" "$(basename "$f")" "$(printf '%s\n' "$r" | grep 'FAIL' | head -3 | tr '\n' ' ')" | tee -a "$out"
    fi
  done
  echo "xong $c" >&2
done
