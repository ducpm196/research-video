#!/usr/bin/env bash
# Hàng đợi dựng hàng loạt cho MỘT khoá: build (lint → tts → render → mp4 → verify) rồi asr cho từng bài, theo thứ tự đưa vào.
# Dùng: bash audit/.build_queue_run.sh CSA L00 L01 …
#   (chạy BẢN SAO .build_queue_run.sh; cập nhật bản sao bằng `cp build_queue.sh x && mv -f x .build_queue_run.sh` —
#    đổi tên giữ nguyên tệp cũ cho hàng đang chạy; ghi đè tại chỗ làm hàng đang chạy đọc lệch, xem production.md)
# Log:
#   audit/<khoá>/logs/<id>.log          lần dựng cuối;  <id>.try<N>.log  các lần dựng bị chặn trước đó (giữ làm bằng chứng)
#   audit/<khoá>/logs/<id>_asr.log      máy nghe
#   audit/<khoá>/logs/queue.out         (do lệnh gọi chuyển hướng) một dòng/bài, có giờ và thời lượng từng bước
#   audit/review/production_log.tsv     một dòng/bài cho MỌI khoá — theo dõi bằng audit/review/prod_watch.py
# Chính sách giọng (người dùng chọn 2026-10-28: “trải nghiệm tốt và ổn định nhất, tránh 2 giọng đan xen”):
#   1. Dựng bằng giọng gốc (vi-VN-NamMinhNeural qua edge-tts; Azure cùng giọng nếu có khoá).
#      Bản thân `lv.py tts` đã thử lại câu hỏng thêm 3 lượt (nghỉ 30/60/120 s) trước khi báo BLOCKED.
#   2. Vẫn bị chặn → chờ 3 phút, dựng lại; vẫn chặn → chờ 10 phút, dựng lại (câu đã đọc nằm trong cache).
#      (trước 2026-10-30: một lần chờ 10 phút; đo CLD: 9/13 bài bị chặn, +15–17 phút/bài, vì lv.py chỉ thử 7 lần/câu)
#   3. Vẫn chặn → ghi out/<khoá>/<id>/voice_override.json = giọng dự phòng trong tools/registry/tts_fallback.yaml và dựng LẠI CẢ BÀI
#      bằng giọng đó (không câu nào giữ giọng gốc). verify FAIL nếu một bài có hai giọng.
#   Không có giọng dự phòng → quay về chờ 1 giờ / lần như cũ (memory quota-wait-hourly), tối đa 24 lần.
# Lỗi khác (lint, render, verify) → ghi FAIL và sang bài sau; không bao giờ bỏ qua cổng kiểm tra.
set -u
# UTF-8 cho mọi lệnh python: tên giọng “Minh Đức” in ra cp1252 sẽ lỗi → FALLBACK rỗng → dự phòng tắt lặng lẽ (lỗi thật 2026-10-28)
export PYTHONIOENCODING=utf-8
# không đệm: log hiện từng dòng khi bài đang dựng (trước đây <id>.log trống tới khi lệnh kết thúc)
export PYTHONUNBUFFERED=1
PY=.venv/Scripts/python
[ -x "$PY" ] || PY=.venv/bin/python
C=$1; shift
c=$(echo "$C" | tr 'A-Z' 'a-z')
mkdir -p "audit/$c/logs" audit/review
PLOG=audit/review/production_log.tsv
[ -f "$PLOG" ] || printf 'kết_thúc\tkhoá\tbài\tkết_quả\tdựng_s\tasr_s\tsố_lần_dựng\tgiọng\ttts\tasr\n' > "$PLOG"
# “NoAudioReceived:” (có dấu hai chấm) = lỗi thật; dòng tổng kết tts in “NoAudioReceived×N” cả khi đã đọc xong → không tính
blocked() { grep -qE "BLOCKED|NoAudioReceived:" "$1"; }
ts() { date '+%Y-%m-%d %H:%M:%S'; }
build() {  # dựng một lần; lần trước (nếu có) được giữ thành <id>.try<N>.log
  if [ -s "$log" ]; then n=$((n + 1)); mv -f "$log" "audit/$c/logs/$id.try$n.log"; fi
  $PY tools/lv.py build "$f" > "$log" 2>&1
}
for id in "$@"; do
  # đọc lại MỖI bài: cấu hình giọng dự phòng điền sau vẫn có hiệu lực mà không phải khởi động lại hàng
  FALLBACK=$($PY -c "import yaml;print((yaml.safe_load(open('tools/registry/tts_fallback.yaml',encoding='utf-8')) or {}).get('voice') or '')" 2>/dev/null)
  [ -f tools/registry/tts_fallback.yaml ] && [ -z "$FALLBACK" ] && echo "$C $id: CẢNH BÁO — không đọc được giọng dự phòng"
  f=$(ls lessons/$c/${id}_*.yaml 2>/dev/null | head -1)
  [ -z "$f" ] && { echo "[$(ts)] $C $id: KHÔNG CÓ ĐẶC TẢ"; continue; }
  log="audit/$c/logs/$id.log"
  rm -f "audit/$c/logs/$id".try*.log "$log"
  n=0; t0=$(date +%s)
  build
  for w in 180 600; do
    blocked "$log" || break
    echo "[$(ts)] $C $id: TTS bị chặn sau các lượt thử trong lv.py, chờ $((w / 60)) phút rồi dựng lại giọng gốc"; sleep $w
    build
  done
  if blocked "$log" && [ -n "$FALLBACK" ]; then
    echo "[$(ts)] $C $id: giọng gốc vẫn bị chặn → dựng CẢ BÀI bằng giọng dự phòng $FALLBACK"
    $PY - "$C" "$id" "$FALLBACK" <<'PYEOF'
import json, sys, datetime
from pathlib import Path
c, i, v = sys.argv[1:4]
d = Path("out") / c / i; d.mkdir(parents=True, exist_ok=True)
(d / "voice_override.json").write_text(json.dumps({"voice": v, "reason": "edge-tts bị chặn sau 3 lượt dựng (build_queue)",
    "at": datetime.datetime.now().isoformat(timespec="seconds")}, ensure_ascii=False), encoding="utf-8")
PYEOF
    build
  fi
  for i in $(seq 1 24); do
    blocked "$log" || break
    echo "[$(ts)] $C $id: TTS bị chặn, chờ 1 giờ (lần $i)"; sleep 3600
    build
  done
  t1=$(date +%s)
  res=$(grep -E "^verify:" "$log" | tail -1)
  ttsl=$(grep -E "^tts: [0-9]+ câu" "$log" | tail -1 | cut -c6-)
  ov=""; voice="gốc"; [ -f "out/$C/$id/voice_override.json" ] && { ov=" [giọng dự phòng]"; voice="dự phòng"; }
  if echo "$res" | grep -q "→ PASS"; then
    $PY tools/lv.py asr "$f" > "audit/$c/logs/${id}_asr.log" 2>&1
    t2=$(date +%s)
    asrl=$(grep '^asr: [0-9]* câu' "audit/$c/logs/${id}_asr.log" | sed 's/ → .*//' | cut -c6-)
    dev=$(grep '^asr: [0-9]* s;' "audit/$c/logs/${id}_asr.log" | sed 's/.*máy nghe: //')
    echo "[$(ts)] $C $id:$ov $res | asr: $asrl | dựng $((t1 - t0)) s ($((n + 1)) lần), asr $((t2 - t1)) s [$dev]"
    printf '%s\t%s\t%s\tPASS\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(ts)" "$C" "$id" $((t1 - t0)) $((t2 - t1)) $((n + 1)) "$voice" "$ttsl" "$asrl; $dev" >> "$PLOG"
  else
    echo "[$(ts)] $C $id: FAIL sau $((t1 - t0)) s — xem $log"; tail -3 "$log"
    printf '%s\t%s\t%s\tFAIL\t%s\t\t%s\t%s\t%s\t\n' "$(ts)" "$C" "$id" $((t1 - t0)) $((n + 1)) "$voice" "$ttsl" >> "$PLOG"
  fi
done
echo "QUEUE_DONE $C"
