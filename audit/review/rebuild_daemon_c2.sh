#!/usr/bin/env bash
# Bản 2 của rebuild_daemon_c.sh: cho phép chạy 2 hàng song song an toàn — mỗi bài được "nhận" bằng mkdir (nguyên tử)
# trong audit/review/rebuild_c.claims/<KHOÁ>_<id>; hàng khác thấy đã nhận thì bỏ qua.
# Hàng: audit/review/rebuild_c.queue ("KHOÁ Lxx" mỗi dòng). Đã dựng: rebuild_c.done. Dừng: tạo rebuild_c.stop.
# Dùng: bash audit/review/rebuild_daemon_c2.sh <tên_hàng>   (log: audit/review/rebuild_c.<tên_hàng>.out)
# Bài cần dựng LẠI lần nữa sau khi đã xong: xoá dòng của nó trong rebuild_c.done và thư mục nhận, rồi để trong hàng.
# Không sửa tệp này khi đang chạy.
cd /d/research-video || exit 1
export PYTHONIOENCODING=utf-8
W=${1:-a}
Q=audit/review/rebuild_c.queue; D=audit/review/rebuild_c.done; CL=audit/review/rebuild_c.claims; LOG=audit/review/rebuild_c.$W.out
mkdir -p "$CL"; touch "$Q" "$D"
echo "DAEMON_START $W $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
while [ ! -f audit/review/rebuild_c.stop ]; do
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
