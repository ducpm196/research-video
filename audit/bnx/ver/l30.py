"""Kiểm độc lập BNX L30 (Chịu lỗi bằng mã). Đường khác với tools/checklib_bnx/l30.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình: Java 21 thuần (thử lại, cầu dao, vách ngăn, xô token, cân bằng tải, quy mô) và Resilience4j 2.3.0 thật
  (jar ở audit/bnx/deps/l30, so sha256 với README trước khi chạy), đầu ra phải bằng từng ký tự đầu ra đã hiện;
- mô hình tham chiếu (alg.bnx_l30_*) đối chiếu với đầu ra thật của Java; bộ đếm quy mô tính lại bằng vòng lặp Python riêng (ver), không dùng hàm của alg;
- cầu dao: thử lại 3 kịch bản (nguồn gốc khác Java) bằng cài đặt Python dựa trên bảng chuyển trạng thái;
- lab chạy lại và so mong_doi.txt.
Thiếu jar / sha256 sai / javac → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l30 as src  # noqa: E402

DEPS = ROOT / "audit" / "bnx" / "deps" / "l30"
LAB = ROOT / "labs" / "BNX" / "L30"


def sha_ok():
    readme = DEPS / "README.md"
    if not readme.exists():
        return None
    want = dict(re.findall(r"\| (\S+\.jar) \| ([0-9a-f]{64}) \|", readme.read_text(encoding="utf-8")))
    if not want:
        return None
    for name, h in want.items():
        f = DEPS / name
        if not f.exists():
            return None
        if hashlib.sha256(f.read_bytes()).hexdigest() != h:
            return False
    return True


# bảng chuyển trạng thái viết khác alg: (trạng thái, kết quả cuộc gọi) → trạng thái kế
def cau_dao_bang(thoi_diem, hong_toi, nguong=3, cho=1000):
    t, hong, mo = "DONG", 0, 0
    that = chan = 0
    log = []
    for ms in thoi_diem:
        if t == "MO" and ms - mo < cho:
            chan += 1
            log.append((ms, "chan"))
            continue
        if t == "MO":
            t = "NUA_MO"
        tot = ms > hong_toi
        that += 1
        if t == "NUA_MO":
            t, hong, mo = ("DONG", 0, mo) if tot else ("MO", hong, ms)
        elif tot:
            hong = 0
        else:
            hong += 1
            if hong >= nguong:
                t, mo = "MO", ms
        log.append((ms, ("tot" if tot else "hong"), t))
    return that, chan, log


def run(rec):
    if not shutil.which("javac"):
        rec("L30", None, "thiếu javac: NOT_VERIFIED")
    else:
        ok = sha_ok()
        if ok is None:
            rec("L30", None, "thiếu jar Resilience4j hoặc README (audit/bnx/deps/l30): NOT_VERIFIED")
        elif not ok:
            rec("L30", False, "sha256 của jar không khớp README")
        else:
            rec("L30", True, "sha256 của 8 jar khớp README")
            lib2.verify_programs(rec, "L30")
            P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L30"}
            out = P["ChayTuCai"].out.splitlines()
            rec("L30", out[0] == "hong 2 lan, toi da 4: thanh cong o lan 3, cho tong 300 ms" and out[1] == "hong 5 lan, toi da 4: that bai sau 4 lan, cho tong 700 ms"
                and alg.bnx_l30_retry(2, 4, 100) == ("ok", 3, 300) and alg.bnx_l30_retry(5, 4, 100) == ("that bai", 4, 700), "thử lại có lùi: 300 ms và 700 ms (Java thật khớp mô hình)")
            line_cd = [l for l in out if l.startswith("t=")]
            that, chan, log = cau_dao_bang([i * 500 for i in range(9)], 2500)
            rec("L30", len(line_cd) == 9 and that == 7 and chan == 2 and "tong: 7 cuoc goi that, 2 cuoc bi chan" in out and alg.bnx_l30_breaker([i * 500 for i in range(9)], 2500) == (7, 2, "DONG"), "cầu dao: 9 lần gọi, 7 thật, 2 chặn (Java = bảng chuyển trạng thái Python = alg)")
            tt = {ms: (rest[0] if len(rest) == 1 else rest[1]) for ms, *rest in log}
            rec("L30", [l.split(" -> ")[-1] if " -> " in l else "chan" for l in line_cd] == [("chan" if x[1] == "chan" else x[2]) for x in log], "chuỗi trạng thái từng lần gọi của Java trùng bảng chuyển trạng thái")
            # lời đọc ví dụ phải khớp nhật ký: 1500 chặn, 2000 thử hỏng → MO, 2500 chặn, 3000 thử tốt → DONG (đọc từ YAML đã sinh)
            lg = {x[0]: x[1:] for x in log}
            ymltxt = next((ROOT / "lessons" / "bnx").glob("L30_*.yaml")).read_text(encoding="utf-8")
            rec("L30", lg[1500] == ("chan",) and lg[2000] == ("hong", "MO") and lg[2500] == ("chan",) and lg[3000] == ("tot", "DONG")
                and "cuộc ở một nghìn năm trăm bị chặn" in ymltxt and "hai cuộc kế tiếp bị chặn" not in ymltxt and "bốn nghìn cuộc gọi" not in ymltxt,
                "nhật ký cầu dao: 1500 chặn, 2000 thử hỏng → MO, 2500 chặn, 3000 thử tốt → DONG; lời đọc khớp; tiêu đề không còn 'bốn nghìn'")
            rec("L30", "else if (++hong >= NGUONG)" in src.J_CAUDAO.code and "hong = 0;" in src.J_CAUDAO.code and src.J_CAUDAO.show_from("void ghi", 10).count("MO") >= 2,
                "CauDao.java (trích) hiện đủ hàm ghi: nhánh nửa mở, tốt xoá bộ đếm, hỏng tăng bộ đếm rồi mở")
            rec("L30", "2 cuoc dang cham: them 3 cuoc -> nhan 0, tu choi 3" in out and "sau khi 2 cuoc cham xong: con 2 cho trong" in out, "vách ngăn: 2 chỗ chiếm hết → 0 nhận 3 từ chối; xong thì trả lại 2 chỗ")
            rec("L30", "12 yeu cau cung luc luc 0 ms: nhan 5, tu choi 7" in out and "12 yeu cau cung luc sau 1 giay: nhan 2" in out and alg.bnx_l30_bucket(5, 2, [(0, 12), (1000, 12)]) == [5, 2], "xô token: 5 nhận 7 từ chối; sau 1 giây nhận 2 (khớp mô hình)")
            rec("L30", "xoay vong: toi da dong thoi may 1 = 2, may 2 = 1" in out and "it ket noi nhat: toi da dong thoi may 1 = 1, may 2 = 1" in out, "cân bằng tải: xoay vòng chồng 2 việc lên máy 1; ít kết nối nhất: 1 và 1")
            qm = [l for l in out if "yeu cau, 10 giay su co" in l]
            nums = [tuple(int(x) for x in re.findall(r"(\d+) yeu cau.*?khong cau dao (\d+) cuoc goi, co cau dao (\d+)", l)[0]) for l in qm]
            rec("L30", nums == [(100, 400, 12), (10000, 40000, 12)] and all(alg.bnx_l30_retry_load(n, 3) == k for n, k, _ in nums), "quy mô: 100 yêu cầu → 400 cuộc gọi, 10 000 → 40 000; có cầu dao luôn 12")
            # đếm quy mô bằng vòng lặp riêng: cầu dao Python với n yêu cầu rải đều trong 10 giây
            for n in (100, 10000):
                th, ch, _ = cau_dao_bang([i * 10000 // n for i in range(n)], 10**9)
                rec("L30", th == 12 and th + ch == n, f"vòng lặp Python riêng: {n} yêu cầu → {th} cuộc gọi thật (12), {ch} bị chặn")
            r4 = P["ChayR4j"].out.splitlines()
            rec("L30", r4 == ["chuyen: State transition from CLOSED to OPEN", "sau 6 cuoc hong: trang thai OPEN, bi chan 2", "chuyen: State transition from OPEN to HALF_OPEN",
                              "chuyen: State transition from HALF_OPEN to CLOSED", "sau khi cho 1,1 giay va 1 cuoc tot: CLOSED"], "Resilience4j thật: CLOSED → OPEN sau 4 cuộc hỏng, 2 bị chặn, rồi OPEN → HALF_OPEN → CLOSED")
            rec("L30", alg.bnx_l30_breaker([0, 100, 200, 300, 400, 500], 10**9)[:2] == (3, 3), "bản tự cài mở sau 3 hỏng, chặn 3 trong 6; thư viện (cửa sổ 4) mở sau 4 hỏng, chặn 2 — khác cách đếm, cùng ba trạng thái")
    rec("L30", alg.bnx_l30_retry(5, 5, 50)[2] == 750 and alg.bnx_l30_bucket(4, 1, [(0, 9), (2000, 9)]) == [4, 2] and alg.bnx_l30_luong_cho(500, 10) == 5000, "quiz: chờ 750 ms; xô token nhận 4 rồi 2; 5 000 luồng chờ")
    # thử lại: r lần thử lại = 1 + r lần gọi; 'thử lại 5 lần' = 6 lần gọi → chờ 50+100+200+400+800 = 1550 (đếm lại bằng vòng lặp riêng)
    cho6 = sum(50 * 2 ** k for k in range(5))
    rec("L30", cho6 == 1550 == alg.bnx_l30_retry(6, 6, 50)[2] and alg.bnx_l30_retry_load(100, 3) == 100 * (1 + 3), "quiz 1: thử lại 5 lần = 6 lần gọi, tổng chờ 1550 ms; r = 3 thử lại → 1 + 3 = 4 cuộc mỗi yêu cầu")
    # quiz câu 3: 50 chỗ, mỗi cuộc giữ ≤ 2 s → ≤ 25 yêu cầu/giây; 500 yêu cầu/giây → từ chối ≥ 95%; 5 000 luồng chỉ khi cuộc gọi treo tới hết hạn 10 s, cuộc 3,5 s → 1 750
    qua = 50 / 2
    rec("L30", qua == alg.bnx_l30_vach_qua(50, 2) == 25 and round(100 * (500 - qua) / 500) == 95 and 500 * 10 == 5000 and 500 * 3.5 == alg.bnx_l30_luong_cho(500, 3.5) == 1750, "quiz 3: vách ngăn 50 chỗ qua tối đa 25 yêu cầu/giây, 475/500 = 95% bị từ chối; 5 000 (treo 10 s) và 1 750 (chậm 3,5 s) luồng chờ")
    # R4j với cấu hình MẶC ĐỊNH của nửa mở (bỏ permittedNumberOfCallsInHalfOpenState(1)): sau 1 cuộc tốt vẫn HALF_OPEN (chạy thật, jar đã so sha256)
    if sha_ok():
        import os
        import tempfile
        code = next(q for q in lib2.PROGRAMS if q.lesson == "L30" and q.name == "R4j").code
        var = code.replace(".permittedNumberOfCallsInHalfOpenState(1).build();", ".build();")
        d = Path(tempfile.mkdtemp())
        (d / "R4j.java").write_text(var, encoding="utf-8")
        cp = os.pathsep.join(str(j) for j in DEPS.glob("*.jar"))
        c1 = subprocess.run(["javac", "-encoding", "UTF-8", "-cp", cp, "-d", str(d), str(d / "R4j.java")], capture_output=True, text=True, encoding="utf-8")
        c2 = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-cp", str(d) + os.pathsep + cp, "R4j"], capture_output=True, text=True, encoding="utf-8")
        rec("L30", var != code and c1.returncode == 0 and "sau khi cho 1,1 giay va 1 cuoc tot: HALF_OPEN" in c2.stdout, "R4j mặc định (không đặt permittedNumberOfCallsInHalfOpenState): sau 1 cuộc tốt vẫn HALF_OPEN; bài đặt =1 nên về CLOSED")
    else:
        rec("L30", None, "thiếu jar: NOT_VERIFIED mặc định nửa mở của Resilience4j")
    r = subprocess.run([sys.executable, "-X", "utf8", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L30", r.returncode == 0 and r.stdout.strip() == (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip(), "lab: loi_giai.py cho đúng mong_doi.txt")
    th, ch, _ = cau_dao_bang([ms for ms in range(0, 3001, 300)], 1499, nguong=2, cho=600)
    rec("L30", (th, ch) == (9, 2) and alg.bnx_l30_breaker(list(range(0, 3001, 300)), 1499, 2, 600)[:2] == (9, 2), "lab: 9 cuộc gọi thật, 2 bị chặn (bảng chuyển trạng thái = alg)")
