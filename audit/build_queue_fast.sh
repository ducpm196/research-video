#!/usr/bin/env bash
# Hàng dựng NHANH: như audit/build_queue.sh (cùng chính sách giọng, cùng log, cùng audit/review/production_log.tsv), thêm
#   (1) dựng bằng tools/lv_fast.py (MP4 10 fps bằng NVENC; giáo án đọc bằng CSafeLoader);
#   (2) máy nghe (ASR) chạy SONG SONG với bài kế tiếp (nhiều nhất 1 ASR + 1 bài đang dựng).
# Dùng:      bash audit/build_queue_fast.sh KHOÁ [Lxx …]      (không ghi bài = mọi bài của khoá)
# Tuỳ chọn:  SKIP_FRESH=1      bỏ qua bài đã dựng đúng đặc tả (lv verify PASS) và đã nghe sạch
#            ALLOW_PARALLEL=1  vẫn chạy khi đang có hàng dựng khác (mặc định TỪ CHỐI)
# Dừng sạch: tạo tệp audit/review/queue_fast.stop → dừng trước bài kế tiếp, đợi ASR đang chạy xong
#            (trên Windows, ngắt tác vụ nền để sót tiến trình con).
# Như build_queue.sh: bash đọc tệp trong lúc chạy → muốn sửa tệp khi hàng đang chạy thì chạy một BẢN SAO.
# Kiểm chứng: audit/perf/fast_pipeline_20261126/REPORT.md
set -u
export PYTHONIOENCODING=utf-8
export PYTHONUNBUFFERED=1
PY=${LV_PY:-.venv/Scripts/python}
[ -x "$PY" ] || PY=.venv/bin/python
LV=${LV_TOOL:-tools/lv_fast.py}
C=${1:?"dùng: bash audit/build_queue_fast.sh KHOÁ [Lxx …]"}; shift
c=$(echo "$C" | tr 'A-Z' 'a-z')
[ $# -gt 0 ] || set -- $(ls lessons/$c/L*_*.yaml 2>/dev/null | sed 's#.*/##; s/_.*//' | sort -u)
[ $# -gt 0 ] || { echo "không có bài nào cho khoá $C"; exit 2; }

STOP=audit/review/queue_fast.stop
LOCK=out/_queue_fast.lock
# không chạy chồng lên hàng dựng khác: tranh GPU/RAM và có thể ghi cùng out/<khoá>/<bài>
if [ "${ALLOW_PARALLEL:-0}" != 1 ] && command -v powershell >/dev/null 2>&1; then
  # python đang dựng/nghe hoặc hàng python; hàng bash cũ (cả lúc đang ngủ chờ giọng, khi không có tiến trình python nào)
  busy=$(powershell -NoProfile -Command '@(Get-CimInstance Win32_Process | Where-Object { ($_.Name -like "python*" -and $_.CommandLine -match "lv(_fast)?\.py[`"]?\s+(build|asr)\s|build_queue\w*\.py") -or ($_.Name -like "bash*" -and $_.CommandLine -match "bash(\.exe)?`"?\s+`"?[^-\s`"][^\s`"]*(build_queue(_run)?|rebuild_\w+)\.sh") }).Count' 2>/dev/null | tr -d '\r\n ')
  if [ "${busy:-0}" != 0 ]; then
    echo "Đang có hàng dựng khác ($busy tiến trình) → KHÔNG chạy. Đợi nó xong, hoặc ALLOW_PARALLEL=1 nếu chắc chắn."
    exit 3
  fi
fi
mkdir -p out
mkdir "$LOCK" 2>/dev/null || { echo "đã có một hàng nhanh khác (nếu lần trước bị ngắt: xoá thư mục $LOCK)"; exit 3; }
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

mkdir -p "audit/$c/logs" audit/review
PLOG=audit/review/production_log.tsv
[ -f "$PLOG" ] || printf 'kết_thúc\tkhoá\tbài\tkết_quả\tdựng_s\tasr_s\tsố_lần_dựng\tgiọng\ttts\tasr\n' > "$PLOG"
# “NoAudioReceived:” (có dấu hai chấm) = lỗi thật; dòng tổng kết tts in “NoAudioReceived×N” cả khi đã đọc xong → không tính
blocked() { grep -qE "BLOCKED|NoAudioReceived:" "$1"; }
ts() { date '+%Y-%m-%d %H:%M:%S'; }
build() {  # dựng một lần; lần trước (nếu có) được giữ thành <id>.try<N>.log
  if [ -s "$log" ]; then n=$((n + 1)); mv -f "$log" "audit/$c/logs/$id.try$n.log"; fi
  $PY "$LV" build "$f" > "$log" 2>&1
}
fresh() {  # SKIP_FRESH=1: video đúng đặc tả hiện tại (verify so mã băm đặc tả/giọng, thời lượng, một giọng)
  [ "${SKIP_FRESH:-0}" = 1 ] && [ -f "out/$C/$id/$id.mp4" ] && $PY "$LV" verify "$f" >/dev/null 2>&1
}
heard() {  # đã nghe sau lần dựng cuối, đủ audio, không còn câu chưa xem xét
  r="out/$C/$id/asr_report.md"; b="out/$C/$id/build_report.json"
  [ -f "$r" ] && [ -f "$b" ] && [ ! "$b" -nt "$r" ] && grep -qE "thiếu audio: 0, .*chưa xem xét: 0[[:space:]]*$" "$r"
}
asr_then_log() {  # chạy nền: mọi biến của bài được chụp lại tại lúc gọi
  ta=$(date +%s)
  $PY "$LV" asr "$f" > "audit/$c/logs/${id}_asr.log" 2>&1
  tb=$(date +%s)
  asrl=$(grep '^asr: [0-9]* câu' "audit/$c/logs/${id}_asr.log" | sed 's/ → .*//' | cut -c6-)
  dev=$(grep '^asr: [0-9]* s;' "audit/$c/logs/${id}_asr.log" | sed 's/.*máy nghe: //')
  echo "[$(ts)] $C $id:$ov $res | asr: $asrl | dựng $dur s ($tries lần), asr $((tb - ta)) s [$dev]"
  printf '%s\t%s\t%s\tPASS\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(ts)" "$C" "$id" "$dur" $((tb - ta)) "$tries" "$voice" "$ttsl" "$asrl; $dev" >> "$PLOG"
}
ASR_PID=""; ASR_ID=""
wait_asr() { [ -z "$ASR_PID" ] || wait "$ASR_PID"; ASR_PID=""; }

end=QUEUE_DONE
for id in "$@"; do
  if [ -f "$STOP" ]; then echo "[$(ts)] gặp $STOP → dừng trước $C $id"; end=QUEUE_STOPPED; break; fi
  # đọc lại MỖI bài: cấu hình giọng dự phòng điền sau vẫn có hiệu lực mà không phải khởi động lại hàng
  FALLBACK=$($PY -c "import yaml;print((yaml.safe_load(open('tools/registry/tts_fallback.yaml',encoding='utf-8')) or {}).get('voice') or '')" 2>/dev/null)
  [ -f tools/registry/tts_fallback.yaml ] && [ -z "$FALLBACK" ] && echo "$C $id: CẢNH BÁO — không đọc được giọng dự phòng"
  f=$(ls lessons/$c/${id}_*.yaml 2>/dev/null | head -1)
  [ -z "$f" ] && { echo "[$(ts)] $C $id: KHÔNG CÓ ĐẶC TẢ"; continue; }
  [ "$id" = "$ASR_ID" ] && wait_asr   # không dựng lại một bài khi ASR của chính nó còn chạy
  log="audit/$c/logs/$id.log"
  ov=""; voice="gốc"
  if fresh; then
    if heard; then echo "[$(ts)] $C $id: đã dựng đúng đặc tả và đã nghe sạch → bỏ qua"; continue; fi
    res="verify: đã đúng đặc tả, không dựng lại (SKIP_FRESH) → PASS"; dur=0; tries=0; ttsl=""
  else
    rm -f "audit/$c/logs/$id".try*.log "$log"
    n=0; t0=$(date +%s)
    build
    for w in ${QUEUE_WAITS:-180 600}; do
      blocked "$log" || break
      echo "[$(ts)] $C $id: TTS bị chặn sau các lượt thử trong lv.py, chờ $w giây rồi dựng lại giọng gốc"; sleep "$w"
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
      echo "[$(ts)] $C $id: TTS bị chặn, chờ ${QUEUE_HOUR_WAIT:-3600} giây (lần $i)"; sleep "${QUEUE_HOUR_WAIT:-3600}"
      build
    done
    t1=$(date +%s); dur=$((t1 - t0)); tries=$((n + 1))
    res=$(grep -E "^verify:" "$log" | tail -1)
    ttsl=$(grep -E "^tts: [0-9]+ câu" "$log" | tail -1 | cut -c6-)
  fi
  [ -f "out/$C/$id/voice_override.json" ] && { ov=" [giọng dự phòng]"; voice="dự phòng"; }
  if echo "$res" | grep -q "→ PASS"; then
    wait_asr            # ASR bài trước xong mới mở ASR bài này: không bao giờ hai ASR cùng lúc
    asr_then_log &
    ASR_PID=$!; ASR_ID=$id
  else
    echo "[$(ts)] $C $id: FAIL sau $dur s — xem $log"; tail -3 "$log"
    printf '%s\t%s\t%s\tFAIL\t%s\t\t%s\t%s\t%s\t\n' "$(ts)" "$C" "$id" "$dur" "$tries" "$voice" "$ttsl" >> "$PLOG"
  fi
done
wait_asr
echo "$end $C"
