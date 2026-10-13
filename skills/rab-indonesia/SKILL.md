---
name: rab-indonesia
description: Susun RAB (Rencana Anggaran Biaya) proyek konstruksi di Indonesia — volume/BoQ, analisis harga satuan pekerjaan (AHSP), harga satuan dasar upah-bahan-alat, overhead & profit, PPN, rekap, dan kurva S. Gunakan saat user minta RAB, estimasi biaya bangunan/jalan/irigasi, hitung volume pekerjaan, AHSP, BoQ, HPS/OE, atau review RAB kontraktor.
---

# RAB Indonesia

Alur baku RAB di Indonesia. Ikuti urutan ini, jangan loncat.

## 0. Cek kesiapan data (WAJIB, sebelum hitung apapun)
Skill ini tidak membawa AHSP resmi atau harga dasar. Minta ke user, satu per satu, lewat pertanyaan singkat:

1. **AHSP resmi**: "Punya file AHSP (Permen PUPR 8/2023 / SNI / punya instansi) dalam PDF atau Excel? Kirim path-nya." Kalau ada: ekstrak item yang dipakai proyek ini ke `ahsp.json` (format di `contoh/proyek.json`), tunjukkan hasilnya ke user untuk dicek. Kalau tidak ada: tandai semua koefisien "asumsi, perlu verifikasi" dan jangan sebut hasilnya RAB final.
2. **Harga satuan dasar**: "Punya daftar HSD/HSPK daerah proyek (tahun berapa)? Atau penawaran supplier?" Simpan ke `harga_dasar` lengkap dengan tanggal dan sumber.
3. **Tarif pajak & overhead**: tanya ketentuan instansi/kontrak (profit %, overhead %, PPN). Jangan pakai default tanpa konfirmasi; cek `references/regulasi.md` lalu minta user memverifikasi tarif terbaru.
4. **Jenis proyek**: kalau user pakai tipe proyek berulang (rumah tinggal, jalan, drainase), tawarkan menyimpan paket AHSP + BoQ yang sudah dikonfirmasi sebagai template di `data/<jenis>.json` untuk dipakai ulang di proyek berikutnya.

Simpan data yang sudah dikonfirmasi di folder kerja user (bukan di dalam skill) supaya sesi berikutnya tidak perlu tanya ulang. Kalau file data sudah ada, baca dulu dan tanya hanya yang kurang atau kedaluwarsa.

## 1. Kumpulkan input (tanya kalau belum ada)
- Jenis proyek (gedung, jalan, jembatan, drainase, irigasi) + lokasi (menentukan harga dasar & kemahalan).
- Gambar kerja / spesifikasi / BoQ. Tanpa gambar → beri estimasi kasar (Rp/m² dari proyek serupa), **labeli "estimasi kasar, bukan RAB"**.
- Sumber harga dasar: daftar harga satuan dasar upah/bahan/alat daerah (HSD/HSPK dari pemda, SIPLah/e-katalog, atau penawaran supplier). Tanggal harga wajib dicatat.
- Tujuan: RAB internal, HPS/OE pengadaan, atau penawaran kontraktor.

## 2. Volume (BoQ)
- Hitung per item pekerjaan, satuan standar (m³, m², m', kg, ls/unit). Tulis rumus volume tiap item supaya bisa diaudit.
- Kelompokkan per divisi: persiapan, tanah, pondasi, beton/struktur, dinding, atap, lantai, finishing, MEP, lain-lain.
- Besi tulangan: konversi dari kg/m³ beton hanya sebagai cek silang, utamakan dari gambar penulangan.

## 3. Harga satuan pekerjaan (AHSP)
- Rumus: **HSP = Σ (koefisien × harga dasar)** untuk tenaga + bahan + alat.
- Koefisien harus dari **AHSP resmi** (Permen PUPR 8/2023 atau SNI yang berlaku) — **jangan mengarang koefisien dari ingatan**. Kalau user belum punya dokumennya, minta file/tabel, atau tandai nilai sebagai "asumsi, perlu verifikasi".
- Untuk item tanpa AHSP baku: analisa sendiri (produktivitas × jam kerja) dan tandai "analisa sendiri".

## 4. Hitung
Isi `proyek.json` (format di `contoh/proyek.json`), lalu:

```bash
python3 scripts/rab.py proyek.json --csv rab.csv
```

Script hitung HSP per item, tambah profit/overhead, jumlah, PPN, total, pembulatan ke ribuan. Cek mandiri: `python3 scripts/test_rab.py`.

## 5. Rekap & lapor
- Tabel: No | Uraian | Satuan | Volume | Harga Satuan | Jumlah, subtotal per divisi, lalu Jumlah → PPN → Total → Dibulatkan → **Terbilang**.
- Sebut asumsi: tanggal & sumber harga, versi AHSP, tarif overhead/profit, tarif PPN.
- Sanity check sebelum kirim: Rp/m² masuk akal vs proyek sejenis; proporsi struktur vs finishing vs MEP wajar; tidak ada item volume 0 / harga 0; satuan konsisten.

## 6. Turunan (kalau diminta)
- **Kurva S**: bobot item = jumlah item ÷ total; sebar per minggu sesuai jadwal.
- **Rekap bahan & upah**: jumlahkan koefisien × volume per komponen untuk daftar belanja.
- **Review RAB kontraktor**: bandingkan volume (dari gambar) dan HSP vs AHSP resmi; tandai selisih >10%.

## Aturan
- Angka pajak & regulasi berubah. Cek `references/regulasi.md`, lalu **verifikasi ke sumber resmi** sebelum dipakai di dokumen kontrak/pengadaan.
- Kalau data kurang, tanya dulu. Jangan isi harga dasar dengan tebakan tanpa label.
- RAB hanya estimasi; tanggung jawab teknis & tanda tangan tetap pada ahli/estimator berwenang.
