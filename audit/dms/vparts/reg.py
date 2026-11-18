"""Sổ đăng ký bộ kiểm DMS: mỗi tệp vparts/lNN.py đăng ký (a) @lab("Lxx"): hàm trả các dòng mong_doi.txt TÍNH LẠI BẰNG CÁCH KHÁC;
(b) @quymo("Lxx"): hàm trả [(tên, đúng/sai)] tính lại các con số của cảnh quy mô."""
LABS, QUY_MO = {}, {}


def lab(lid):
    def deco(fn):
        LABS[lid] = fn
        return fn
    return deco


def quymo(lid):
    def deco(fn):
        QUY_MO[lid] = fn
        return fn
    return deco
