#!/usr/bin/env bash
# Chờ dịch vụ giọng đọc hoạt động lại: thử MỘT câu ngắn mỗi giờ (memory quota-wait-hourly), tối đa 24 lần; in TTS_OK khi được.
PY=.venv/Scripts/python
for i in $(seq 1 24); do
  if $PY -c "
import asyncio, edge_tts, sys
async def m(): await edge_tts.Communicate('Xin chào bạn.', 'vi-VN-NamMinhNeural').save(sys.argv[1])
asyncio.run(m())" "out/_cache/tts_probe_ok.mp3" >/dev/null 2>&1; then echo "TTS_OK sau $((i-1)) giờ chờ"; exit 0; fi
  echo "TTS chưa có ($(date -u +%FT%TZ)), chờ 1 giờ"; sleep 3600
done
echo "TTS_FAIL sau 24 giờ"; exit 1
