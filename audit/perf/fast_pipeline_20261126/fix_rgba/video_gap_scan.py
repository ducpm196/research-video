"""Quét video đã dựng tìm lỗi mất slide/hụt hình (chỉ đọc bảng chỉ mục MP4, không giải mã, không dùng GPU).

Dùng từ thư mục gốc:  .venv/Scripts/python -B audit/perf/fast_pipeline_20261126/fix_rgba/video_gap_scan.py [KHOÁ …]
Mã thoát: 0 = không có video hỏng, 1 = có.
"""
import json
import os
import struct
import sys
import time
from pathlib import Path


def boxes(f, start, end):
    pos = start
    while pos + 8 <= end:
        f.seek(pos)
        size, kind = struct.unpack(">I4s", f.read(8))
        head = 8
        if size == 1:
            size, head = struct.unpack(">Q", f.read(8))[0], 16
        elif size == 0:
            size = end - pos
        if size < head:
            return
        yield kind, pos + head, pos + size
        pos += size


def video_problem(mp4, fps, total):
    with open(mp4, "rb") as f:
        moov = next(((a, b) for k, a, b in boxes(f, 0, os.path.getsize(mp4)) if k == b"moov"), None)
        for kind, a, b in boxes(f, *moov) if moov else ():
            if kind != b"trak":
                continue
            found, todo = {}, [(a, b)]
            while todo:
                for k, s, e in boxes(f, *todo.pop()):
                    if k in (b"mdia", b"minf", b"stbl"):
                        todo.append((s, e))
                    elif k in (b"mdhd", b"hdlr", b"stts"):
                        f.seek(s)
                        found[k] = f.read(e - s)
            if found[b"hdlr"][8:12] != b"vide":
                continue
            m = found[b"mdhd"]
            scale, dur = struct.unpack(">IQ", m[20:32]) if m[0] == 1 else struct.unpack(">II", m[12:20])
            t, table = 0.0, found[b"stts"]
            for i in range(struct.unpack(">I", table[4:8])[0]):
                count, delta = struct.unpack(">II", table[8 + 8 * i:16 + 8 * i])
                if delta / scale > 1.5 / fps:
                    return f"khung ở {t:.1f} s bị giữ {delta / scale:.1f} s"
                t += count * delta / scale
            if dur / scale < total - 0.15:
                return f"phần hình dài {dur / scale:.1f} s, ngắn hơn timeline {total:.1f} s"
            return None
    return "không đọc được phần hình của MP4"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out = Path(__file__).resolve().parents[4] / "out"
    wanted = set(sys.argv[1:])
    checked, bad, busy = 0, [], []
    for report in sorted(out.glob("*/L*/build_report.json")):
        od = report.parent
        mp4 = od / (od.name + ".mp4")
        if (wanted and od.parent.name not in wanted) or not mp4.exists():
            continue
        # build_report.json được ghi SAU mp4: mp4 mới hơn và vừa đổi trong 3 phút = đang dựng, chưa kết luận
        written = mp4.stat().st_mtime
        if written > report.stat().st_mtime + 1 and time.time() - written < 180:
            busy.append(f"{od.parent.name}/{od.name}")
            continue
        try:
            d = json.loads(report.read_text(encoding="utf-8"))
            fps = 10 if "10fps" in d.get("video_encoder", "") else 30
            problem = video_problem(mp4, fps, float(d["timeline_seconds"]))
        except Exception as e:  # bài đang được dựng lại
            problem = f"không kiểm được: {type(e).__name__}"
        checked += 1
        if problem:
            bad.append(f"{od.parent.name}/{od.name}: {problem}")
    print("\n".join(bad))
    if busy:
        print(f"đang dựng, chưa kiểm (quét lại sau): {', '.join(busy)}")
    print(f"kiểm {checked} video, hỏng {len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
