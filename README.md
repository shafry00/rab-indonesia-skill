# rab-indonesia

Claude skill untuk menyusun **RAB (Rencana Anggaran Biaya)** proyek konstruksi di Indonesia: BoQ → AHSP → harga satuan → rekap, plus kalkulator Python tanpa dependency.

## Install

```bash
git clone https://github.com/shafry00/rab-indonesia-skill
cp -r rab-indonesia-skill/skills/rab-indonesia ~/.claude/skills/
```

Atau lewat CLI skills: `npx skills add shafry00/rab-indonesia-skill --skill rab-indonesia --agent claude-code`.

## Pakai

Minta Claude: *"Buatkan RAB rumah 2 lantai 120 m² di Bandung"* atau *"Review RAB kontraktor ini"*. Untuk hitung manual:

```bash
python3 skills/rab-indonesia/scripts/rab.py skills/rab-indonesia/contoh/proyek.json --csv rab.csv
```

Skill akan meminta data yang dibutuhkan di awal (file AHSP resmi, harga dasar daerah, tarif overhead/PPN) dan menyimpannya untuk proyek berikutnya, jadi siapkan dokumen-dokumen itu.

## Penting

- Koefisien & harga di `contoh/proyek.json` adalah **contoh ilustrasi**, bukan acuan resmi. Pakai AHSP resmi (Permen PUPR 8/2023 / SNI) dan harga dasar daerah proyek.
- Ringkasan regulasi di `references/regulasi.md` perlu diverifikasi ke sumber resmi.
- Hasil adalah estimasi; bukan pengganti ahli/estimator berwenang.

Kontribusi (data AHSP, template per jenis proyek) diterima lewat PR. Lisensi MIT.
