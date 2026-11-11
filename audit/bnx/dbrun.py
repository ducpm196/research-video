"""Chạy SQL thật trên Oracle và SQL Server trong Docker — để mã PL/SQL, T-SQL trên màn hình của khoá BNX được chạy NGUYÊN VĂN.

Container (dựng 2026-11-11, ảnh đã kéo về máy):
  bnx-ora  gvenzl/oracle-free:23-slim   → banner "Oracle AI Database 26ai Free Release 23.26.3.0.0"; người dùng bnx/bnx_pass, dịch vụ FREEPDB1
  bnx-mss  mcr.microsoft.com/mssql/server:2022-latest → "Microsoft SQL Server 2022 (RTM-CU27-GDR) 16.0.4315.2"; sa / Bnx_Pass_2026!
Khởi động lại sau khi máy tắt:  docker start bnx-ora bnx-mss   (Oracle cần ~1 phút tới "DATABASE IS READY TO USE!")
Dựng lại từ đầu: xem audit/bnx/BRIEF.md mục 8 "Môi trường".

Dùng trong audit/bnx/ver/lNN.py:
    from dbrun import ora, mss
    out = ora(sql_text)    # sqlplus -s, tự thêm SET SERVEROUTPUT ON, WHENEVER SQLERROR CONTINUE, exit; trả stdout (str)
    out = mss(sql_text)    # sqlcmd -b không dùng (để thấy lỗi ở giữa), -C tin chứng chỉ tự ký, -h -1 bỏ tiêu đề cột; trả stdout+stderr
Mỗi lần gọi là một phiên mới. Muốn sạch: tự DROP/CREATE ở đầu đoạn SQL (hoặc dùng schema/database riêng cho từng bài: bnx_lNN).
"""
import os
import subprocess

ORA = ("bnx-ora", "bnx/bnx_pass@//localhost/FREEPDB1")
MSS = ("bnx-mss", "Bnx_Pass_2026!")
ENV = dict(os.environ, MSYS_NO_PATHCONV="1")


def _run(args, text, timeout=180):
    r = subprocess.run(args, input=text, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV, timeout=timeout)
    return r.stdout + (("\n" + r.stderr) if r.stderr.strip() else "")


def ready():
    """(oracle_ok, mssql_ok) — hai container đang chạy và trả lời được truy vấn."""
    o = "1" in ora("SELECT 1 AS x FROM dual;")
    m = "1" in mss("SELECT 1;")
    return o, m


def ora(sql, header=True):
    pre = ("SET SERVEROUTPUT ON SIZE UNLIMITED\nSET FEEDBACK OFF\nSET LINESIZE 200\nSET PAGESIZE 100\nSET TRIMOUT ON\n"
           "WHENEVER SQLERROR CONTINUE\n") if header else ""
    return _run(["docker", "exec", "-i", ORA[0], "sqlplus", "-s", "-L", ORA[1]], pre + sql.rstrip() + "\nexit\n")


def mss(sql, db=None):
    args = ["docker", "exec", "-i", MSS[0], "/opt/mssql-tools18/bin/sqlcmd", "-S", "localhost", "-U", "sa", "-P", MSS[1], "-C", "-h", "-1", "-W"]
    if db:
        args += ["-d", db]
    return _run(args, sql.rstrip() + "\nGO\n")


if __name__ == "__main__":
    print(ready())
