import re
import subprocess
import sys
from pathlib import Path

import pytest  # noqa: F401

LOI = """def tong_n_dau(ds, n):
    tong = 0
    for i in range(1, n):
        tong = tong + ds[i]
    return tong
"""
DUNG = LOI.replace("range(1, n)", "range(n)")
KIEM = """import pytest
from tong import tong_n_dau

DS = [10, 20, 30, 40, 50]


@pytest.mark.parametrize("n, mong_doi", [(0, 0), (1, 10), (2, 30), (3, 60), (4, 100), (5, 150)])
def test_tong(n, mong_doi):
    assert tong_n_dau(DS, n) == mong_doi
"""


def chay(ma):
    Path("tong.py").write_text(ma, encoding="utf-8")
    Path("test_tong.py").write_text(KIEM, encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=no", "-p", "no:cacheprovider", "test_tong.py"], capture_output=True, text=True)
    return re.sub(r" in [0-9.]+s", "", r.stdout.strip().split("\n")[-1])


print("Ban loi:", chay(LOI))
print("Ban sua:", chay(DUNG))
