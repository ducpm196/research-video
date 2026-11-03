#!/usr/bin/env bash
# Dựng + máy nghe mọi bài mẫu hồ sơ chuyên ngành (examples/profiles/*_L01.yaml). Ghi log examples/profiles/<hồ sơ>_build.log.
cd "$(dirname "$0")/../.."
export PYTHONIOENCODING=utf-8 PYTHONUNBUFFERED=1
for f in examples/profiles/*_L0[2-9].yaml; do
  n=$(basename "$f" .yaml)
  # mỗi mẫu một id riêng trong out/DEMO/ để không ghi đè nhau
  .venv/Scripts/python tools/lv.py build "$f" > "examples/profiles/${n}_build.log" 2>&1
  .venv/Scripts/python tools/lv.py asr "$f" >> "examples/profiles/${n}_build.log" 2>&1
  echo "$n: $(grep -h 'verify:' examples/profiles/${n}_build.log | tail -1 | cut -c1-90) | $(grep -h '^asr: [0-9]* câu' examples/profiles/${n}_build.log | tail -1 | cut -c1-90)"
done
