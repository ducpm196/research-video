"""Khoá cứng mọi script sinh/nâng cấp hàng loạt sau AF4 (BN-04).
Muốn chạy để đo độ trôi (WP-0.10): đặt biến môi trường AF5_ALLOW_GEN=1."""
import os
import sys

if os.environ.get("AF5_ALLOW_GEN") != "1":
    sys.stderr.write(
        "FROZEN (BN-04): generator đã khoá từ AF5; hãy sửa trực tiếp YAML bài học và chạy kiểm. "
        "Để đo độ trôi, đặt AF5_ALLOW_GEN=1.\n"
    )
    raise SystemExit(2)
