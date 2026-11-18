# Lab PYT L12 — Viết ca kiểm bắt lỗi lệch một

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Hàm có lỗi **lệch một** (`range(1, n)` bỏ phần tử đầu), và bản đúng (`range(n)`):

```python
def tong_n_dau(ds, n):
    tong = 0
    for i in range(1, n):      # LỖI: phải là range(n)
        tong = tong + ds[i]
    return tong
```

Viết `kiem_thu.py` (số minh hoạ; khác ví dụ trong bài):

1. Ghi `tong.py` (lần lượt bản **lỗi** rồi bản **đúng**) và `test_tong.py` có `DS = [10, 20, 30, 40, 50]` và `@pytest.mark.parametrize("n, mong_doi", […])` với **6 ca** `n = 0, 1, 2, 3, 4, 5`. **Tự tính tay** giá trị mong đợi (tổng `n` phần tử đầu), không chạy mã để lấy.
2. Với mỗi bản: chạy `python -m pytest -q --tb=no -p no:cacheprovider test_tong.py` bằng `subprocess.run([sys.executable, "-m", "pytest", …], capture_output=True, text=True)` (`sys.executable` là đường dẫn tới chính bản Python đang chạy bạn, để chương trình con dùng cùng môi trường ảo; `capture_output=True` giữ đầu ra lại thay vì in ra màn hình; `text=True` cho `stdout` là chữ, không phải byte; `--tb=no` bỏ chi tiết ca đỏ; `-p no:cacheprovider` tắt thư mục nhớ tạm); lấy dòng cuối của `stdout`, bỏ phần ` in …s`; in `Ban loi: <dòng>` rồi `Ban sua: <dòng>`.
3. Nhớ `import pytest` ở đầu tệp (máy chấm cần thấy thư viện này để dùng môi trường đã cài).

Chạy: `python kiem_thu.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L12 kiem_thu.py`.
