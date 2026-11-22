# Lab CVI L01 — Lọc ảnh bằng tích chập Sobel S_x

Viết hàm tính **tích chập** 2D (có lật bộ lọc 180 độ `kx[2 - r][2 - c]`) với bộ lọc Sobel `S_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]` trên hai vùng `3 × 3`: (1) vùng cạnh có cột phải bằng `12`, hai cột trái bằng `0`; (2) vùng phẳng toàn số `5` (tính trực tiếp qua hàm, không gán cứng).

Định dạng đầu ra (1 dòng):
`sobel_edge_x=<số nguyên> flat_region=<số nguyên>`
