# Phụ thuộc của bài BNX L23 (scikit-learn, ONNX, ONNX Runtime, rừng cô lập)

Thư viện ngoài nằm trong **môi trường riêng `audit/bnx/deps/l23/venv`** (Python 3.13.5, `python -m venv`), KHÔNG cài vào `.venv`, không sửa `requirements.txt`.
Dựng lại: `python -m venv audit/bnx/deps/l23/venv` rồi `audit/bnx/deps/l23/venv/Scripts/python.exe -m pip install scikit-learn==1.9.1 skl2onnx==1.20.0 onnxruntime==1.31.1 numpy==2.5.4`
(pip kéo thêm các gói còn lại trong bảng). Bản ghi (`pip freeze`, kiểm 2026-11-12): đúng 15 gói dưới đây.

sha256 là của tệp wheel trên PyPI cho Windows x64, Python 3.13, tải lại bằng `pip download --no-deps --only-binary=:all:` đúng phiên bản đã cài (2026-11-12).

| Gói | Phiên bản | Tệp wheel | sha256 |
|---|---|---|---|
| scikit-learn | 1.9.1 | scikit_learn-1.9.1-cp313-cp313-win_amd64.whl (8 237 244 byte) | 2070f271e5375dc42c6bb93b461ab1c0aa5841d4009267e0cfd95a39dca94a43 |
| skl2onnx | 1.20.0 | skl2onnx-1.20.0-py3-none-any.whl (317 169) | 30cac34803d1776c14b336ae945e48ef28debfc339215acde1cc04b963ed3f7b |
| onnxruntime | 1.31.1 | onnxruntime-1.31.1-cp313-cp313-win_amd64.whl (14 888 304) | 0558f29d5f6ac09957390c9c5495931485ee8ae7f0ce781ccee86a0ae5c2348b |
| numpy | 2.5.4 | numpy-2.5.4-cp313-cp313-win_amd64.whl (12 566 113) | 8b4d2fd2d34e5f8c9235ee787de5631a37a28402b15cb80814df973d2be54129 |
| onnx | 1.23.2 | onnx-1.23.2-cp312-abi3-win_amd64.whl (7 872 489) | 9b382ba898a7c142a0801d03cf04ecabced96c1543c7b643a86f0928143802de |
| scipy | 1.18.1 | scipy-1.18.1-cp313-cp313-win_amd64.whl (36 622 841) | 559ed65f60c1af5a03f3912605a1b5114f522c7c32fb23c3376ae8f03219fe28 |
| joblib | 1.6.0 | joblib-1.6.0-py3-none-any.whl (306 115) | 3dbbf9f6e4b592a2357b854608e980fe6390d131d7a82f011a377ef2ebef7aba |
| threadpoolctl | 3.8.0 | threadpoolctl-3.8.0-py3-none-any.whl (32 091) | f1b49c82704d50f13ffae019c727b0fa4f6791a58f48f06a09c45face1be66da |
| protobuf | 7.36.2 | protobuf-7.36.2-cp310-abi3-win_amd64.whl (456 514) | a300819d441e078a5608c0d3c709796bb548136058fda017ae51d425b44fd353 |
| flatbuffers | 25.12.19 | flatbuffers-25.12.19-py2.py3-none-any.whl (26 661) | 7634f50c427838bb021c2d66a3d1168e9d199b0607e6329399f04846d42e20b4 |
| ml_dtypes | 0.6.0 | ml_dtypes-0.6.0-cp313-cp313-win_amd64.whl (439 357) | fb87f46b4f7ad7b5d3ad8f4b452b024bd4229d44c8ff934798c1fe656210387a |
| packaging | 26.3 | packaging-26.3-py3-none-any.whl (129 956) | d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c |
| narwhals | 2.28.0 | narwhals-2.28.0-py3-none-any.whl (490 591) | 1f69d6385ec30e2fa6e1fdeb37c562ecabd0f713f6f3e3b58a668c5c9df9567f |
| cloudpickle | 3.1.2 | cloudpickle-3.1.2-py3-none-any.whl (22 228) | 9acb47f6afd73f60dc1df93bb801b472f05ff42fa6c84167d25cb206be1fbf4a |
| typing_extensions | 4.16.0 | typing_extensions-4.16.0-py3-none-any.whl (45 571) | 481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8 |

Ghi chú:
- Một tệp rỗng `scipy-1.18.1-cp313-cp313-win_amd64.whl` (0 byte, dấu vết của một lần tải dở) nằm trong `venv/Lib/site-packages`; đã xoá 2026-11-12, không ảnh hưởng thư viện đã cài.
- Cách dùng: `audit/bnx/ver/l23.py` chạy các khối mã của bài bằng `audit/bnx/deps/l23/venv/Scripts/python.exe`; sổ `audit/bnx/screen/l23.yaml` chạy các khối bằng `.venv` sau khi đặt `sys.path` vào
  `audit/bnx/deps/l23/venv/Lib/site-packages` (nguồn `L23_venv`; cùng Python 3.13.5 nên cùng ABI). Thiếu thư mục này: trả mã 97 và dòng `NOT_VERIFIED` trên stderr (cổng FAIL có nhãn, không PASS lặng lẽ).
- Bài không dùng mạng, Docker hay GPU. Dữ liệu sinh bằng `numpy.random.default_rng` với hạt giống cố định (42, 7, 99); rừng cô lập dùng `random_state=42`.
- `skl2onnx.to_onnx` mặc định của bản 1.20.0 báo lỗi với miền `ai.onnx.ml` bản 4 trên mô hình này; phải khai `target_opset={"": 17, "ai.onnx.ml": 3}` (bài dạy đúng điều này như một lỗi mới dựng).
