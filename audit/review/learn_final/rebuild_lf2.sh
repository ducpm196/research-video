#!/usr/bin/env bash
# Hàng dựng lại của đợt LF2 (bản sao có tham số của audit/review/rebuild_daemon_c2.sh, tệp riêng để không lẫn hàng cũ).
# Hàng: audit/review/learn_final/rebuild.queue ("KHOÁ Lxx" mỗi dòng). Đã dựng: rebuild.done. Nhận bài: rebuild.claims/<KHOÁ>_<id> (mkdir nguyên tử).
# Dừng: tạo audit/review/learn_final/rebuild.stop (dừng sau bài đang dựng).
# Dùng: bash audit/review/learn_final/rebuild_lf2.sh <tên_luồng>   (log: audit/review/learn_final/logs/rebuild.<tên_luồng>.out)
# Mỗi bài: bash audit/.build_queue_run.sh KHOÁ Lxx (lint → tts → render → mp4 → verify → asr; chính sách giọng như production.md).
# Bài cần dựng LẠI: xoá dòng của nó trong rebuild.done và thư mục nhận, để nó trong hàng. Không sửa tệp này khi đang chạy.
cd /d/research-video || exit 1
export PYTHONIOENCODING=utf-8
W=${1:-a}
B=audit/review/learn_final
Q=$B/rebuild.queue; D=$B/rebuild.done; CL=$B/rebuild.claims; LOG=$B/logs/rebuild.$W.out
mkdir -p "$CL" "$B/logs"; touch "$Q" "$D"
echo "DAEMON_START $W $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
while [ ! -f "$B/rebuild.stop" ]; do
  next=""
  while read -r c id _; do
    [ -z "$c" ] && continue
    grep -q "^$c $id " "$D" && continue
    if mkdir "$CL/${c}_$id" 2>/dev/null; then next="$c $id"; break; fi
  done < "$Q"
  if [ -z "$next" ]; then sleep 120; continue; fi
  set -- $next
  mkdir -p "audit/$(echo "$1" | tr A-Z a-z)/logs"
  bash audit/.build_queue_run.sh "$1" "$2" < /dev/null >> "$LOG" 2>&1
  echo "$1 $2 $(date -u +%Y-%m-%dT%H:%M:%SZ) $W" >> "$D"
done
echo "DAEMON_STOP $W $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
