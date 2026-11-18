"""Kiểm độc lập BNX L29 (CQRS và Event Sourcing cho sổ tiền). Đường khác với tools/checklib_bnx/l29.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình (Python 3 + sqlite3) và so từng ký tự với đầu ra đã hiện;
- số dư phát lại tính lại bằng SQL (SUM CASE trên bảng sqlite thật), không dùng vòng lặp của bài; trigger chặn sửa/xoá kiểm bằng chính sqlite;
- số sự kiện phải đọc (có/không bản chụp) đếm bằng vòng lặp từng sự kiện với bản chụp thật (lưu số dư mỗi k sự kiện, dựng lại và so với phát lại từ đầu);
- đọc trễ: mô phỏng bộ chiếu từng bước và so với số dư đúng;
- lab chạy lại và so mong_doi.txt."""
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l29 as src  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L29"


def sql_so_du(su_kien):
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE s (seq INTEGER PRIMARY KEY, loai TEXT, tien INTEGER)")
    db.executemany("INSERT INTO s (loai, tien) VALUES (?, ?)", su_kien)
    return db.execute("SELECT COALESCE(SUM(CASE loai WHEN 'NAP' THEN tien ELSE -tien END), 0) FROM s").fetchone()[0]


def doc_voi_ban_chup(n, k, kho):
    """Dựng số dư tại sự kiện n bằng bản chụp thật: lưu số dư mỗi k sự kiện, nạp bản chụp gần nhất rồi đọc từng sự kiện; trả (số dư, số sự kiện đã đọc)."""
    ban = {0: 0}
    so_du = 0
    for i, (loai, tien) in enumerate(kho[:n], 1):
        so_du += tien if loai == "NAP" else -tien
        if k and i % k == 0:
            ban[i] = so_du
    muc = max(i for i in ban if i <= n) if k else 0
    so_du, doc = ban[muc], 0
    for loai, tien in kho[muc:n]:
        so_du += tien if loai == "NAP" else -tien
        doc += 1
    return so_du, doc


def run(rec):
    lib2.verify_programs(rec, "L29")
    P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L29"}
    rec("L29", P["KhoSuKien"].out.splitlines() == ["sua su kien: kho su kien chi them, khong sua", "xoa su kien: kho su kien chi them, khong xoa", "so su kien: 3"], "trigger chặn UPDATE và DELETE; kho còn 3 sự kiện")
    kho = [("NAP", 1000), ("RUT", 300), ("NAP", 50), ("RUT", 120)]
    rec("L29", alg.bnx_l29_replay(kho) == sql_so_du(kho) == 630, "số dư phát lại 630 = SUM CASE bằng SQL thật")
    rec("L29", P["PhatLai"].out.splitlines()[:4] == ["sau su kien 1: 1000", "sau su kien 2: 700", "sau su kien 3: 750", "sau su kien 4: 630"], "bốn số dư trung gian 1000, 700, 750, 630")
    kho2 = kho + [("RUT", 500)]
    kho3 = kho2 + [("NAP", 500), ("RUT", 50)]
    rec("L29", sql_so_du(kho2) == 130 and sql_so_du(kho3) == 580 and P["BuChu"].out.splitlines() == ["sau su kien sai: 130", "sau khi bu: 580 | 7 su kien"], "sự kiện sai → 130; sau bù và ghi đúng → 580, kho 7 sự kiện (SQL tính lại)")
    rec("L29", sql_so_du(kho3) == alg.bnx_l29_replay(kho3) == 630 - 50, "sự kiện bù có tác dụng như sửa: 580 = 630 − 50")
    # đọc trễ: bộ chiếu từng bước
    sk3 = [("NAP", 1000), ("RUT", 300), ("NAP", 50)]
    chieu2 = alg.bnx_l29_replay(sk3[:2])
    rec("L29", P["DocTre"].out.splitlines() == ["doc sau khi chieu 2/3 su kien: 700 (da xu ly 2 / 3 )", "doc sau khi chieu het: 750 (da xu ly 3 / 3 )"] and chieu2 == sql_so_du(sk3[:2]) == 700 and sql_so_du(sk3) == 750, "đọc trễ: mới chiếu 2/3 → 700, chiếu hết → 750")
    # bản chụp thật
    kho_lon = [("NAP" if i % 2 == 0 else "RUT", i % 97 + 1) for i in range(2500500)]
    for n, k, muon in ((2500, 1000, 500), (2500500, 1000, 500)):
        sd, doc = doc_voi_ban_chup(n, k, kho_lon)
        sd0, doc0 = doc_voi_ban_chup(n, 0, kho_lon)
        rec("L29", doc == muon == alg.bnx_l29_events_to_read(n, k) and doc0 == n == alg.bnx_l29_events_to_read(n, 0) and sd == sd0, f"n = {n}: bản chụp thật đọc {doc} sự kiện (không bản chụp {doc0}), số dư giống nhau")
    rec("L29", P["BanChup"].out.splitlines() == ["2500 su kien: khong ban chup doc 2500, chup moi 1000 su kien doc 500", "2500500 su kien: khong ban chup doc 2500500, chup moi 1000 su kien doc 500"], "đầu ra BanChup khớp")
    rec("L29", P["QuyMoPhat"].out.splitlines()[0].startswith("1000 su kien: da doc 1000 su kien") and P["QuyMoPhat"].out.splitlines()[1].startswith("1000000 su kien: da doc 1000000 su kien"), "quy mô: đọc đúng 10³ và 10⁶ sự kiện (đếm thật)")
    rec("L29", alg.bnx_l29_events_to_read(999999, 1000) == 999 and 7300000 % 5000 == 0 and alg.bnx_l29_events_to_read(7300000, 5000) == 0, "tối đa 999 sự kiện đọc; 7 300 000 chia hết 5 000 → đọc 0")
    # giới hạn của trigger: người có quyền DDL gỡ được rồi sửa lịch sử (sqlite thật, cùng định nghĩa trigger của bài)
    db = sqlite3.connect(":memory:")
    db.executescript("CREATE TABLE su_kien (seq INTEGER PRIMARY KEY AUTOINCREMENT, tk TEXT, loai TEXT, tien INTEGER); CREATE TRIGGER khong_sua BEFORE UPDATE ON su_kien BEGIN SELECT RAISE(ABORT, 'x'); END;")
    db.execute("INSERT INTO su_kien (tk, loai, tien) VALUES ('001', 'RUT', 300)")
    try:
        db.execute("UPDATE su_kien SET tien = 900 WHERE seq = 1")
        chan = False
    except sqlite3.DatabaseError:
        chan = True
    db.execute("DROP TRIGGER khong_sua")
    db.execute("UPDATE su_kien SET tien = 900 WHERE seq = 1")
    rec("L29", chan and db.execute("SELECT tien FROM su_kien WHERE seq = 1").fetchone()[0] == 900, "trigger chặn UPDATE nhưng DROP TRIGGER rồi UPDATE thành công: bài nói giới hạn (quyền quản trị, chuỗi băm), không nói tuyệt đối")
    # số dư âm của QuyMoPhat: dữ liệu sinh i%2 (0 nạp, 1 rút), tiền i%97+1, đếm bằng đường khác (SQL trên 1000 và 10^6 dòng)
    dbq = sqlite3.connect(":memory:")
    dbq.execute("CREATE TABLE sk (seq INTEGER PRIMARY KEY, loai INTEGER, tien INTEGER)")
    dbq.executemany("INSERT INTO sk (loai, tien) VALUES (?, ?)", ((i % 2, i % 97 + 1) for i in range(1000000)))
    s1000 = dbq.execute("SELECT SUM(CASE loai WHEN 0 THEN tien ELSE -tien END) FROM sk WHERE seq <= 1000").fetchone()[0]
    s1m = dbq.execute("SELECT SUM(CASE loai WHEN 0 THEN tien ELSE -tien END) FROM sk").fetchone()[0]
    rec("L29", (s1000, s1m) == (-15, 35) and f"so du {s1000}" in P["QuyMoPhat"].out and f"so du {s1m}" in P["QuyMoPhat"].out, "quymo: số dư -15 (10³) và 35 (10⁶) tính lại bằng SQL; âm vì dữ liệu sinh không chặn rút quá số dư")
    q1 = [("NAP", 800), ("RUT", 150), ("RUT", 90), ("NAP", 40)]
    rec("L29", sql_so_du(q1) == 600 and sql_so_du(q1 + [("NAP", 150), ("RUT", 15)]) == 735, "quiz câu 1: 600 và sau bù 735 (SQL)")
    r = subprocess.run([sys.executable, "-X", "utf8", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L29", r.returncode == 0 and r.stdout.strip() == (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip(), "lab: loi_giai.py cho đúng mong_doi.txt")
    lk = [("NAP", 500), ("RUT", 100), ("NAP", 200), ("RUT", 50), ("NAP", 25), ("RUT", 75)]
    rec("L29", sql_so_du(lk) == 500 and sql_so_du(lk[:4]) == 550 and sql_so_du(lk + [("RUT", 300), ("NAP", 300)]) == 500, "lab: 500, bản chụp 550 sau 4 sự kiện, sau bù 500 (SQL)")
    # trigger "khong_sua/khong_xoa" của bài KHÔNG chặn mọi cách sửa: INSERT OR REPLACE ghi đè sự kiện cùng seq, DROP TABLE vẫn chạy (sqlite thật, đúng 2 trigger của bài)
    dbl = sqlite3.connect(":memory:")
    dbl.executescript(src.PY_KHO.code.split('db.executescript("""')[1].split('""")')[0])
    dbl.execute("INSERT INTO su_kien (tk, loai, tien) VALUES ('001', 'RUT', 300)")
    dbl.execute("INSERT OR REPLACE INTO su_kien (seq, tk, loai, tien) VALUES (1, '001', 'RUT', 900)")
    ghi_de = dbl.execute("SELECT tien FROM su_kien WHERE seq = 1").fetchone()[0]
    dbl.execute("DROP TABLE su_kien")
    ton_tai = dbl.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = 'su_kien'").fetchone()[0]
    rec("L29", ghi_de == 900 and ton_tai == 0, f"trigger của bài bị lách: INSERT OR REPLACE ghi đè 300 → {ghi_de}; DROP TABLE xoá bảng (sqlite {sqlite3.sqlite_version})")
