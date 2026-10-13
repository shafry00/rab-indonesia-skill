"""Cek cepat: python3 test_rab.py"""
from rab import hitung

p = {
    "harga_dasar": {"a": 100, "b": 10},
    "ahsp": {"x": {"tenaga": {"a": 2}, "bahan": {"b": 5}, "alat": {}}},  # 200 + 50 = 250
    "boq": [{"uraian": "t", "satuan": "m2", "volume": 4, "ahsp": "x"}],
    "overhead": {"profit_persen": 10, "ppn_persen": 10},
}
h = hitung(p)
assert abs(h["baris"][0]["hs_langsung"] - 250) < 1e-9
assert abs(h["jumlah"] - 1100) < 1e-9  # 250*1.1*4
assert abs(h["total"] - 1210) < 1e-9
try:
    hitung({**p, "boq": [{"uraian": "t", "satuan": "m", "volume": 1, "ahsp": "nope"}]})
    raise SystemExit("harus error")
except KeyError:
    pass
print("ok")
