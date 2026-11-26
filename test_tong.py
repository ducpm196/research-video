import pytest
from tong import tong_n_dau

DS = [10, 20, 30, 40, 50]


@pytest.mark.parametrize("n, mong_doi", [(0, 0), (1, 10), (2, 30), (3, 60), (4, 100), (5, 150)])
def test_tong(n, mong_doi):
    assert tong_n_dau(DS, n) == mong_doi
