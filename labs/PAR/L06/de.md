# Lab PAR L06 — Vector hoá SIMD và phần dư vô hướng

Đọc `n reg_bits elem_bits` từ stdin (ví dụ `100 512 32`, với SIMD = một lệnh, nhiều dữ liệu). Tính số làn thanh ghi vector (`simd_lanes = reg_bits // elem_bits`), số lệnh vector (`vec_ops = n // lanes`) và số phần tử phần dư (`scalar_tail = n % lanes`).
In đúng 1 dòng `simd_lanes=<int> vec_ops=<int> scalar_tail=<int>`.
