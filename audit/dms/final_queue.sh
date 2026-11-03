#!/usr/bin/env bash
# Hàng đợi cuối đợt DMS (2026-10-27). Chạy từ gốc dự án, sau khi lô L14–L19 xong.
# 1) L13 (lời đọc bỏ tên Bézout) và L01 (viết lại 2 câu ngắn): build + asr.
# 2) Mọi bài DMS có mp4 CŨ hơn player.css (đã đổi CSS dòng mã; lúc làm đối chứng dương CSS cũ được đặt tạm): build lại.
# 3) 13 bài CS112 có khung “viền-đè-chữ” với CSS cũ (audit/layout_scan.py): build lại (TTS đã có cache, chỉ dựng lại hình).
# TTS bị chặn → chờ 1 giờ rồi thử lại (memory quota-wait-hourly).
set -u
PY=.venv/Scripts/python
build() {   # $1 = đường dẫn bài, $2 = tệp log
  for i in 1 2 3 4 5 6; do
    $PY tools/lv.py build "$1" > "$2" 2>&1 && return 0
    if grep -q "BLOCKED" "$2"; then echo "$1 blocked $i, chờ 1h"; sleep 3600; else return 1; fi
  done
}
mkdir -p audit/dms/logs audit/rebuild_logs
for f in lessons/dms/L13_so_hoc_mo_dun.yaml lessons/dms/L01_tuong_duong_de_morgan.yaml; do
  id=$(basename "$f" | cut -d_ -f1)
  build "$f" "audit/dms/logs/$id.log"; tail -2 "audit/dms/logs/$id.log" | head -1
  $PY tools/lv.py asr "$f" > "audit/dms/logs/${id}_asr.log" 2>&1; grep "^asr:" "audit/dms/logs/${id}_asr.log"
done
for f in lessons/dms/*.yaml; do
  id=$(basename "$f" | cut -d_ -f1)
  if [ "out/DMS/$id/$id.mp4" -ot tools/templates/player.css ]; then
    build "$f" "audit/dms/logs/${id}_css.log"; echo "css-rebuild $id: $(tail -2 "audit/dms/logs/${id}_css.log" | head -1)"
  fi
done
# + L05 L21 L26: có câu nhấn vào một cột (.row > .col.focus đổi khoảng cách viền 2026-10-28)
for id in L00 L03 L05 L07 L08 L10 L14 L16 L17 L18 L21 L23 L24 L25 L26 L28; do
  f=$(ls lessons/cs112/${id}_*.yaml)
  build "$f" "audit/rebuild_logs/cs112_${id}_css.log"; echo "cs112 $id: $(tail -2 "audit/rebuild_logs/cs112_${id}_css.log" | head -1)"
done
# CS115: hai bài có câu nhấn vào một cột
for id in L13 L14; do
  f=$(ls lessons/cs115/${id}_*.yaml)
  build "$f" "audit/rebuild_logs/cs115_${id}_css.log"; echo "cs115 $id: $(tail -2 "audit/rebuild_logs/cs115_${id}_css.log" | head -1)"
done
echo FINAL_DONE
