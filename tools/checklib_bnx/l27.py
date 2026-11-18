"""BNX L27 — SOAP/WSDL và SFTP: mô hình tham chiếu của máy chủ phong bì thử (mã HTTP theo ca), đối soát tệp lô (số dòng rồi mã băm),
tỉ lệ độ nặng phong bì so với JSON, số khối 64 KiB phải đọc khi băm theo luồng. Chỉ thư viện chuẩn, không mạng.
Kiểm độc lập ở audit/bnx/ver/l27.py (chạy THẬT máy chủ/khách HTTP của JDK 21, bộ phân tích XML, Python hashlib; đếm lại khối bằng đường khác)."""


def bnx_l27_soap_status(so_tai_khoan, co_doctype):
    """Máy chủ thử của bài: có khai báo kiểu tài liệu → 400; số 001 → 200; số khác → 500 kèm Fault."""
    if co_doctype:
        return 400
    return 200 if so_tai_khoan == "001" else 500


def bnx_l27_batch_check(so_ghi, so_that, ma_dung):
    """Đối soát tệp lô: số dòng trước (rẻ), mã băm sau."""
    if so_that != so_ghi:
        return "THIEU DONG"
    return "OK" if ma_dung else "SAI MA BAM"


def bnx_l27_sha_len():
    return 64   # sha256 = 256 bit = 64 chữ số thập lục phân


def bnx_l27_ratio(a, b):
    return round(a / b, 1)


def bnx_l27_chunks(n_byte, khoi=65536):
    """Số khối 64 KiB (làm tròn lên) khi đọc theo luồng."""
    return -(-n_byte // khoi)


def bnx_l27_wsdl_counts():
    """(message, portType, operation, binding, service) của tệp WSDL mẫu trong bài."""
    return (2, 1, 1, 1, 1)
