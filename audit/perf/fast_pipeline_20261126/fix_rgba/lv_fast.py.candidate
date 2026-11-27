"""lv_fast — lv.py cộng hai tối ưu tốc độ, KHÔNG sửa lv.py (đo và kiểm chứng: audit/perf/fast_pipeline_20261126/REPORT.md).

1) Bước ghép MP4: 10 khung/giây bằng h264_nvenc (card NVIDIA); NVENC lỗi → tự lùi về libx264 10 khung/giây.
   Timeline, phụ đề, chương, âm thanh giữ nguyên (FPS = 30 của lv.py vẫn quyết định thời lượng từng khung hình).
2) Đọc TỆP GIÁO ÁN curriculum/*.yaml bằng yaml.CSafeLoader (libyaml; 54 tệp là phần lớn thời gian đọc YAML khi lint), vẫn cấm
   khoá trùng. Tệp bài học, registry và mọi tệp khác vẫn qua bộ đọc cũ của lv.py (CSafeLoader dễ dãi hơn ở TAB, một số ký tự
   xuống dòng lạ và vài lỗi cú pháp); giáo án có các ký tự đó, hoặc lỗi, cũng đọc bằng bộ cũ để báo lỗi y như lv.py.
3) Trước khi ghép: đưa ảnh khung khác định dạng về RGB (lỗi mất slide có sẵn trong lv.py). Sau khi ghép: phần hình phải
   không có khung bị giữ lâu và phủ hết timeline, nếu không thì báo lỗi.

Dùng y hệt lv.py:   python tools/lv_fast.py build lessons/<khoá>/Lxx_*.yaml
Biến môi trường:    LV_FAST_ENC = nvenc (mặc định) | x264 | off      LV_FAST_FPS = 10      LV_FAST_YAML = 1 | 0
Lệnh của lv.py không đổi: hàng dựng đang gọi tools/lv.py không bị ảnh hưởng.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lv  # noqa: E402

ENC = os.environ.get("LV_FAST_ENC", "nvenc").strip().lower()
if ENC not in ("nvenc", "x264", "off"):
    sys.exit(f"ENV ERROR: LV_FAST_ENC={ENC!r} (chỉ nhận nvenc | x264 | off)")
OUT_FPS = int(os.environ.get("LV_FAST_FPS", "10"))
if not 5 <= OUT_FPS <= lv.FPS:
    sys.exit(f"ENV ERROR: LV_FAST_FPS={OUT_FPS} phải trong 5..{lv.FPS}")


# ───────────── 1) ghép MP4 ─────────────
def _orig_video_args():
    """Đoạn tham số hình mà lv.cmd_build tạo ra; chỉ thay khi khớp CHÍNH XÁC."""
    return ["-vf", f"fps={lv.FPS},format=yuv420p", "-c:v", "libx264", "-tune", "stillimage", "-crf", "20"]


def _video_args(codec):
    # khung khoá cách nhau cùng khoảng THỜI GIAN như cũ (x264 mặc định 250 khung ở 30 fps ≈ 8,3 giây) để tua video như trước
    gop = max(1, round(250 * OUT_FPS / lv.FPS))
    vf = ["-vf", f"fps={OUT_FPS},format=yuv420p"]
    # -bf 0: không B-frame, mốc giải mã = mốc hiển thị (av_scan đo đúng: hình−tiếng -0,03 s thay vì -0,33 s; tệp còn nhỏ hơn)
    if codec == "h264_nvenc":
        return vf + ["-c:v", "h264_nvenc", "-preset", "p4", "-tune", "hq", "-profile:v", "high",
                     "-rc", "vbr", "-cq", "23", "-b:v", "0", "-g", str(gop), "-bf", "0"]
    return vf + ["-c:v", "libx264", "-tune", "stillimage", "-crf", "20", "-g", str(gop), "-bf", "0"]


def _find(cmd, part):
    return next((i for i in range(len(cmd) - len(part) + 1) if cmd[i:i + len(part)] == part), None)


# ───────────── 1b) ảnh khung cùng định dạng + cổng kiểm phần hình ─────────────
# render thỉnh thoảng trả MỘT ảnh RGBA (vài chục điểm ảnh alpha<255) giữa các ảnh RGB. ffmpeg dựng lại bộ lọc giữa chừng
# → mất slide hoặc hụt đầu video, verify vẫn PASS (đo 2026-11-26: 33 video trong out/, cả bản dựng bằng lv.py).
_PNG_SIGNATURE = bytes((137, 80, 78, 71, 13, 10, 26, 10))


def _png_format(p):
    with open(p, "rb") as f:
        head = f.read(26)
    if head[:8] != _PNG_SIGNATURE or head[12:16] != b"IHDR":
        raise RuntimeError(f"[lv_fast] không phải PNG: {p}")
    return struct.unpack(">IIBB", head[16:26])   # rộng, cao, số bit, kiểu màu (2 = RGB, 6 = RGBA)


def _normalize_frames(ffmpeg, concat_list):
    """Nếu ảnh trong danh sách ghép khác định dạng nhau: đổi các ảnh không phải RGB 8 bit về RGB (alpha vốn bị bỏ khi ra yuv420p)."""
    names = [ln.split("'")[1] for ln in concat_list.read_text(encoding="utf-8").splitlines() if ln.startswith("file '")]
    fmts = {p: _png_format(p) for p in sorted({concat_list.parent / n for n in names})}
    if len({f[:2] for f in fmts.values()}) > 1:
        raise RuntimeError("[lv_fast] ảnh khung khác kích thước nhau → không ghép (render lại)")
    if len(set(fmts.values())) <= 1:
        return 0
    odd = [p for p, f in fmts.items() if f[2:] != (8, 2)]
    for p in odd:
        tmp = p.with_name(p.stem + ".rgb.png")
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", str(p), "-frames:v", "1", "-pix_fmt", "rgb24", str(tmp)], check=True)
        os.replace(tmp, p)
    print(f"[lv_fast] đổi {len(odd)} ảnh khung khác định dạng về RGB: {', '.join(p.name for p in odd[:5])}", flush=True)
    return len(odd)


def _mp4_boxes(f, start, end):
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
    """None nếu phần hình ổn; nếu không: có khung bị giữ lâu (mất slide) hoặc không phủ hết timeline. Chỉ đọc bảng chỉ mục MP4."""
    with open(mp4, "rb") as f:
        moov = next(((a, b) for k, a, b in _mp4_boxes(f, 0, os.path.getsize(mp4)) if k == b"moov"), None)
        for kind, a, b in _mp4_boxes(f, *moov) if moov else ():
            if kind != b"trak":
                continue
            found, todo = {}, [(a, b)]
            while todo:
                for k, s, e in _mp4_boxes(f, *todo.pop()):
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


class _Subprocess:
    """Đứng vào chỗ module subprocess BÊN TRONG lv: chỉ đổi đúng lệnh ghép MP4, mọi lệnh khác chuyển thẳng."""

    def __init__(self):
        self.used = None

    def __getattr__(self, name):
        return getattr(subprocess, name)

    def run(self, cmd, *args, **kwargs):
        if not (isinstance(cmd, list) and "concat" in cmd and str(cmd[-1]).endswith(".mp4")):
            return subprocess.run(cmd, *args, **kwargs)
        base = Path(kwargs.get("cwd") or ".")
        _normalize_frames(cmd[0], base / cmd[cmd.index("-i") + 1])
        self.used = None
        res = None
        if ENC != "off":
            i = _find(cmd, _orig_video_args())
            if i is not None:
                res = self._encode(cmd, i, args, kwargs)
            else:
                print("[lv_fast] CẢNH BÁO: lệnh ghép MP4 trong lv.py đã đổi → chạy nguyên lệnh gốc (cần cập nhật lv_fast.py)", flush=True)
        if res is None:
            res = subprocess.run(cmd, *args, **kwargs)
        if res.returncode == 0 and "-t" in cmd:
            mp4 = base / cmd[-1]
            bad = video_problem(mp4, OUT_FPS if self.used else lv.FPS, float(cmd[cmd.index("-t") + 1]))
            if bad:
                mp4.replace(mp4.with_name(mp4.stem + ".broken.mp4"))   # mất tệp .mp4 → hàng dựng không coi bài là đã xong
                raise RuntimeError(f"[lv_fast] VIDEO HỎNG: {bad} → đổi tên thành {mp4.stem}.broken.mp4")
        return res

    def _encode(self, cmd, i, args, kwargs):
        n = len(_orig_video_args())
        # Ở 10 fps, -shortest cắt mất đuôi âm thanh (đo CLC L07 2026-11-26: thiếu 1568 mẫu = 0,065 s so với bản 30 fps);
        # -t <timeline> của lv.py đã cắt đúng độ dài, bỏ -shortest thì tiếng đủ từng mẫu. Không có -t thì giữ nguyên.
        if "-t" in cmd:
            cmd = [x for x in cmd if x != "-shortest"]
            i = _find(cmd, _orig_video_args())
        order = ["h264_nvenc", "libx264"] if ENC == "nvenc" else ["libx264"]
        for k, codec in enumerate(order):
            last = k + 1 == len(order)
            try:
                res = subprocess.run(cmd[:i] + _video_args(codec) + cmd[i + n:], *args, **kwargs)
            except subprocess.CalledProcessError as e:
                if last:
                    raise
                print(f"[lv_fast] {codec} lỗi (mã {e.returncode}) → lùi về {order[k + 1]}", flush=True)
                continue
            if res.returncode == 0:
                self.used = f"{codec}@{OUT_FPS}fps"
                return res
            if last:
                return res
            print(f"[lv_fast] {codec} lỗi (mã {res.returncode}) → lùi về {order[k + 1]}", flush=True)


_PROXY = _Subprocess()
lv.subprocess = _PROXY

# ───────────── 2) giáo án YAML bằng libyaml ─────────────
YAML_FAST = os.environ.get("LV_FAST_YAML", "1") != "0" and hasattr(yaml, "CSafeLoader") and hasattr(lv, "_no_dup_mapping")
if YAML_FAST:
    class _CStrictLoader(yaml.CSafeLoader):
        pass

    _CStrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, lv._no_dup_mapping)
    _orig_load_yaml = lv.load_yaml

    _CURRICULUM = (lv.ROOT / "curriculum").resolve()
    # ký tự mà libyaml dễ dãi hơn PyYAML thuần: TAB, NEL, U+2028, U+2029, BOM
    _STRICT_CHARS = tuple(chr(c) for c in (0x09, 0x85, 0x2028, 0x2029, 0xFEFF))

    def _load_yaml_c(p):
        path = Path(p)
        if path.resolve().parent == _CURRICULUM:
            text = path.read_text(encoding="utf-8")
            if not any(c in text for c in _STRICT_CHARS):
                try:
                    return yaml.load(text, Loader=_CStrictLoader)
                except yaml.YAMLError:
                    pass
        return _orig_load_yaml(p)   # mọi tệp khác, và mọi lỗi (kể cả khoá trùng): đúng bộ đọc và thông điệp của lv.py

    lv.load_yaml = _load_yaml_c


def _annotate(path):
    """Ghi vào build_report.json bộ mã hoá đã dùng (khoá thêm; verify và hàng dựng không đọc khoá này)."""
    rep = lv.out_dir(lv.load_spec(path)) / "build_report.json"
    d = json.loads(rep.read_text(encoding="utf-8"))
    d["video_encoder"] = _PROXY.used or f"libx264@{lv.FPS}fps (lệnh gốc lv.py)"
    rep.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[lv_fast] video: {d['video_encoder']}; giáo án đọc bằng {'CSafeLoader' if YAML_FAST else 'SafeLoader'}", flush=True)


def main():
    rc = lv.main()
    if rc == 0 and sys.argv[1:2] == ["build"] and len(sys.argv) > 2:
        try:
            _annotate(sys.argv[2])
        except Exception as e:   # chỉ là ghi chú: không được biến bài đã dựng PASS thành FAIL
            print(f"[lv_fast] không ghi được video_encoder vào build_report.json: {type(e).__name__}: {e}", flush=True)
    return rc


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
