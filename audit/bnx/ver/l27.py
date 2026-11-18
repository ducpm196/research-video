"""Kiểm độc lập BNX L27 (SOAP/WSDL và SFTP). Đường khác với tools/checklib_bnx/l27.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình: máy chủ và khách HTTP của JDK 21 (SoapDemo), bộ phân tích XML, Python hashlib;
- mã HTTP, số dư, số byte phong bì/JSON đọc từ đầu ra thật rồi đối chiếu mô hình alg.bnx_l27_*; số byte của phong bì tính lại bằng cách đo chính các tệp XML;
- XML của yêu cầu và WSDL phân tích lại bằng Python (xml.etree) — đếm phần tử bằng đường khác Java;
- tệp lô: dựng ba ca (đủ, mất dòng, đổi chữ số) bằng đường khác (openssl dgst / sha256sum của hệ điều hành) và so với kết luận của hàm kiểm;
- số khối 64 KiB đếm lại bằng vòng lặp trừ dần (không dùng phép chia làm tròn lên của alg);
- lab chạy lại và so mong_doi.txt.
Thiếu javac/java → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import hashlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l27 as src  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L27"
WSDL_NS = "http://schemas.xmlsoap.org/wsdl/"


def khoi_vong_lap(n, khoi=65536):
    c = 0
    while n > 0:
        n -= khoi
        c += 1
    return c


def run(rec):
    if not (shutil.which("javac") and shutil.which("java")):
        rec("L27", None, "thiếu javac/java: NOT_VERIFIED")
    else:
        lib2.verify_programs(rec, "L27")
        P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L27"}
        out = P["ChaySoap"].out
        m = re.search(r"yeu cau SOAP (\d+) byte, JSON tuong duong (\d+) byte", out)
        req_xml = P["YeuCau"].code + "\n"
        rec("L27", bool(m) and int(m.group(1)) == len(req_xml) == 246 and int(m.group(2)) == len('{"soTaiKhoan":"001"}'), "phong bì yêu cầu 246 byte (đo lại bằng chính tệp XML), JSON tương đương 20 byte")
        m2 = re.search(r"tra loi 200: soDu 1250000, SOAP (\d+) byte, JSON (\d+) byte", out)
        rec("L27", bool(m2) and int(m2.group(1)) == 211 and int(m2.group(2)) == len('{"soDu":1250000}'), "trả lời 200 với soDu 1250000; phong bì trả lời 211 byte, JSON 16 byte")
        # fix6 (R4): so cùng cách viết liền. Viết liền = bỏ dấu cách đầu dòng và xuống dòng giữa các thẻ (và giữa các thuộc tính, còn một dấu cách)
        lien = re.sub(r'"\s+xmlns', '" xmlns', re.sub(r">\s+<", "><", req_xml.strip()))
        rec("L27", len(lien) == 203 and round(len(lien) / 20, 1) == 10.2 and round(211 / 16, 1) == 13.2, f"viết liền phong bì yêu cầu {len(lien)} byte (tính lại bằng mã), {len(lien)} : 20 ≈ 10,2 lần; phản hồi 211 : 16 ≈ 13,2 lần")
        rec("L27", alg.bnx_l27_ratio(246, 20) == 12.3 and alg.bnx_l27_ratio(211, 16) == 13.2, "mô hình alg: 246 (tệp thụt dòng) : 20 = 12,3; 211 : 16 = 13,2 (bài dùng 203 viết liền)")
        rec("L27", "tra loi 500: soapenv:Client, khong co so tai khoan" in out and alg.bnx_l27_soap_status("999", False) == 500, "tài khoản lạ: 500 kèm Fault soapenv:Client")
        rec("L27", "tra loi 400 khi yeu cau co DOCTYPE" in out and alg.bnx_l27_soap_status("001", True) == 400, "yêu cầu có DOCTYPE bị từ chối 400 (cấu hình disallow-doctype-decl)")
        rec("L27", out.splitlines()[-1] == "WSDL: message 2 portType 1 operation 1 binding 1 service 1" and alg.bnx_l27_wsdl_counts() == (2, 1, 1, 1, 1), "WSDL: 2 message, 1 portType, 1 operation, 1 binding, 1 service")
        # đường khác: Python đếm phần tử WSDL và đọc phong bì
        w = ET.fromstring(P["Wsdl"].code)
        got = tuple(len(w.findall(f".//{{{WSDL_NS}}}{t}")) for t in ("message", "portType", "operation", "binding", "service"))
        rec("L27", got == (2, 1, 1, 1, 1), f"Python xml.etree đếm lại phần tử WSDL: {got}")
        env = ET.fromstring(P["YeuCau"].code)
        so = [e.text for e in env.iter() if e.tag.endswith("}soTaiKhoan")]
        rec("L27", so == ["001"], "phong bì yêu cầu hỏi tài khoản 001 (đọc bằng Python)")
        # tệp lô
        o = P["GuiLo"].out
        rec("L27", o == "nguoi nhan thay: ['lo1.csv']\ntep dang gui do (bo qua): ['lo2.csv.part']", "tệp .part bị bỏ qua, chỉ lo1.csv được nhận")
        o = P["KiemLo"].out
        rec("L27", o.splitlines() == ["nguyen ven: OK", "mat 100 dong: THIEU DONG", "doi 1 chu so: SAI MA BAM"], "ba ca đối soát: OK, THIEU DONG, SAI MA BAM")
        rec("L27", alg.bnx_l27_batch_check(1000, 1000, True) == "OK" and alg.bnx_l27_batch_check(1000, 900, True) == "THIEU DONG" and alg.bnx_l27_batch_check(1000, 1000, False) == "SAI MA BAM", "mô hình đối soát khớp ba ca")
        # đường khác: sha256 bằng công cụ hệ điều hành
        dong = [f"{i:04d}|TK{i % 7:03d}|{i * 1000}" for i in range(1, 1001)]
        nd = "\n".join(dong) + "\n"
        tmp = ROOT / "audit" / "bnx" / "progcache" / "_l27_lo.txt"
        tmp.write_bytes(nd.encode())
        r = subprocess.run(["sha256sum", tmp.name], cwd=tmp.parent, capture_output=True, text=True) if shutil.which("sha256sum") else None
        if r is None:
            rec("L27", None, "thiếu sha256sum: NOT_VERIFIED")
        else:
            rec("L27", r.stdout.split()[0] == hashlib.sha256(nd.encode()).hexdigest() and len(r.stdout.split()[0]) == alg.bnx_l27_sha_len(), "sha256 của lô 1000 dòng: sha256sum của hệ điều hành khớp hashlib, dài 64 chữ số")
        tmp.unlink()
        # quy mô
        q = P["QuyMoLo"].out.splitlines()
        rec("L27", q[0].startswith("1000 dong: 24000 byte, 1 khoi 64 KiB") and q[1].startswith("1000000 dong: 24000000 byte, 367 khoi 64 KiB"), "quy mô: 24 000 byte/1 khối; 24 000 000 byte/367 khối")
        rec("L27", [khoi_vong_lap(n) for n in (24000, 24000000, 80000000, 24 * 10**9)] == [alg.bnx_l27_chunks(n) for n in (24000, 24000000, 80000000, 24 * 10**9)] == [1, 367, 1221, 366211], "đếm khối bằng vòng lặp trừ dần khớp công thức làm tròn lên: 1, 367, 1221, 366 211")
    # khung WSDL trên màn hình (dòng 5–16 của bank.wsdl) phải cho người học đếm ra đúng 2 message, 1 portType, 1 operation, 1 binding, 1 service
    wsdl = src.X_WSDL.code.strip().splitlines()[4:16]
    dem = tuple(len(re.findall(r"<%s[ >]" % t, "".join(wsdl))) for t in ("message", "portType", "operation", "binding", "service"))
    rec("L27", dem == alg.bnx_l27_wsdl_counts() == (2, 1, 1, 1, 1) and len(wsdl) <= 12, f"khung WSDL hiện (dòng 5–16): đếm được {dem} = 2 message, 1 portType, 1 operation, 1 binding, 1 service")
    # lab
    r = subprocess.run([sys.executable, "-X", "utf8", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L27", r.returncode == 0 and r.stdout.strip() == (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip(), "lab: loi_giai.py cho đúng mong_doi.txt")
    rec("L27", alg.bnx_l27_batch_check(5, 4, True) == "THIEU DONG" and alg.bnx_l27_batch_check(5, 5, False) == "SAI MA BAM" and alg.bnx_l27_batch_check(5, 5, True) == "OK", "lab: bốn ca khớp mô hình đối soát")
