"""fix6 CS112 L18 (đợt 2): định nghĩa tại chỗ 'đệ quy thô' và 'ngăn xếp'. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l18b.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L18")
edit(T, "<p>Viết đệ quy thẳng theo hệ thức: tính", "<p>Viết đệ quy thẳng theo hệ thức (gọi là <b>đệ quy thô</b>): tính")
edit(T, "Nếu viết đệ quy thẳng theo hệ thức, tính số thứ 40", "Nếu viết đệ quy thẳng theo hệ thức, gọi là đệ quy thô, tính số thứ 40")
edit(T, "ghi nhớ từ trên xuống dùng một khung ngăn xếp cho mỗi tầng đệ quy: Python", "ghi nhớ từ trên xuống dùng một khung <b>ngăn xếp</b> (vùng nhớ ghi các lời gọi hàm đang chạy dở) cho mỗi tầng đệ quy: Python")
edit(T, "Ghi nhớ từ trên xuống dùng một khung ngăn xếp cho mỗi tầng đệ quy.", "Ghi nhớ từ trên xuống dùng một khung ngăn xếp, tức vùng nhớ ghi các lời gọi hàm đang chạy dở, cho mỗi tầng đệ quy.")
regen("L18")
