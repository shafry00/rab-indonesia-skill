#!/usr/bin/env python3
"""Hitung RAB (Rencana Anggaran Biaya) dari JSON: harga dasar + AHSP + BoQ.

Pakai: python3 rab.py proyek.json [--csv out.csv]
Tanpa dependency (stdlib saja).
"""
import csv
import json
import sys


def harga_satuan(ahsp, harga):
    """Jumlah koefisien x harga dasar per komponen. Return (rincian, total)."""
    rincian, total = {"tenaga": 0.0, "bahan": 0.0, "alat": 0.0}, 0.0
    for kat in rincian:
        for kode, koef in ahsp.get(kat, {}).items():
            if kode not in harga:
                raise KeyError(f"harga dasar '{kode}' tidak ada")
            rincian[kat] += koef * harga[kode]
    total = sum(rincian.values())
    return rincian, total


def hitung(p):
    harga, ahsp = p["harga_dasar"], p["ahsp"]
    o = p.get("overhead", {})
    baris, jumlah = [], 0.0
    for item in p["boq"]:
        if item["ahsp"] not in ahsp:
            raise KeyError(f"AHSP '{item['ahsp']}' tidak ada (uraian: {item['uraian']})")
        r, hs = harga_satuan(ahsp[item["ahsp"]], harga)
        hs_ok = hs * (1 + o.get("profit_persen", 0) / 100)  # OH&P per satuan
        total = hs_ok * item["volume"]
        jumlah += total
        baris.append({**item, "hs_langsung": hs, "hs_dgn_overhead": hs_ok, "jumlah": total, **r})
    ppn = jumlah * o.get("ppn_persen", 0) / 100
    return {
        "baris": baris,
        "jumlah": jumlah,
        "ppn": ppn,
        "total": jumlah + ppn,
        "dibulatkan": round((jumlah + ppn) / 1000) * 1000,
    }


def rp(x):
    return "Rp " + f"{x:,.0f}".replace(",", ".")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        p = json.load(f)
    h = hitung(p)
    for b in h["baris"]:
        print(f"{b['uraian']:<34}{b['volume']:>9.2f} {b['satuan']:<4}"
              f"@{rp(b['hs_dgn_overhead']):>15} = {rp(b['jumlah']):>18}")
    print(f"{'JUMLAH':<60}{rp(h['jumlah']):>18}")
    print(f"{'PPN':<60}{rp(h['ppn']):>18}")
    print(f"{'TOTAL':<60}{rp(h['total']):>18}")
    print(f"{'DIBULATKAN':<60}{rp(h['dibulatkan']):>18}")
    if "--csv" in sys.argv:
        out = sys.argv[sys.argv.index("--csv") + 1]
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["uraian", "satuan", "volume", "tenaga", "bahan", "alat",
                                              "hs_langsung", "hs_dgn_overhead", "jumlah"],
                               extrasaction="ignore")
            w.writeheader()
            w.writerows(h["baris"])


if __name__ == "__main__":
    main()
