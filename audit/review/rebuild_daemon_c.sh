#!/usr/bin/env bash
# Đợt đọc kiểm C (2026-11-09): hàng dựng lại cuốn chiếu, TUẦN TỰ (render song song làm ffmpeg/ASR hết RAM).
# Hàng: audit/review/rebuild_c.queue — mỗi dòng "KHOÁ Lxx"; người điều phối nối thêm dòng khi một tác tử đọc kiểm xong.
# Đã dựng: audit/review/rebuild_c.done (dòng "KHOÁ Lxx <giờ UTC>"). Dừng: tạo tệp audit/review/rebuild_c.stop.
# Mỗi bài gọi audit/.build_queue_run.sh (lint → tts → render → mp4 → verify, rồi asr), log nối vào audit/review/rebuild_c.out.
# Không sửa tệp này khi đang chạy (bash đọc script theo dòng); dữ liệu nằm ở tệp hàng.
cd /d/research-video || exit 1
export PYTHONIOENCODING=utf-8
Q=audit/review/rebuild_c.queue; D=audit/review/rebuild_c.done; LOG=audit/review/rebuild_c.out
touch "$Q" "$D"
echo "DAEMON_START $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
while [ ! -f audit/review/rebuild_c.stop ]; do
  next=""
  while read -r c id _; do
    [ -z "$c" ] && continue
    grep -q "^$c $id " "$D" || { next="$c $id"; break; }
  done < "$Q"
  if [ -z "$next" ]; then sleep 120; continue; fi
  set -- $next
  mkdir -p "audit/$(echo "$1" | tr A-Z a-z)/logs"
  bash audit/.build_queue_run.sh "$1" "$2" < /dev/null >> "$LOG" 2>&1
  echo "$1 $2 $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$D"
done
echo "DAEMON_STOP $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
