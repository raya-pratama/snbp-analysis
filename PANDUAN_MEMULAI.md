# 🎓 Panduan Memulai Proyek Analisis SNBP Jawa Timur
Semua persiapan awal sudah saya buat, kamu tinggal ikuti langkah di bawah untuk jalanin dashboard di laptopmu.

---

## 📦 Apa yang sudah saya siapkan untukmu?
1.  ✅ Struktur folder proyek yang rapi
2.  ✅ File daftar library yang harus diinstall (`requirements.txt`)
3.  ✅ Data awal bersih untuk UPN Jatim 2024-2026 (dari data resmi situs PMB UPN Jatim) + data contoh untuk ITS, UNAIR, UB, UM, UNESA agar kamu bisa langsung lihat dashboardnya jalan
4.  ✅ Kode dashboard Streamlit yang sudah jadi dan langsung bisa dijalankan
5.  ✅ Semua perhitungan rasio keketatan sudah otomatis di dalam kode

---

## 🛠️ Apa yang perlu kamu install di laptop?
Semua software GRATIS, cuma butuh koneksi internet saat install pertama:
1.  **Python 3.10 atau yang lebih baru**: Download dari https://www.python.org/downloads/
    - Saat install, JANGAN LUPA centang opsi `Add Python to PATH`
2.  **Code Editor (opsional tapi sangat disarankan)**: VS Code - https://code.visualstudio.com/ (gratis)

---

## 🚀 Langkah Pertama Menjalankan Project
Buka terminal/command prompt di folder proyek ini, lalu jalankan perintah berurutan:

### 1. Buat virtual environment (agar projectmu tidak berantakan dengan library lain di laptop)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```
Kalau berhasil, di awal baris terminal kamu akan ada tulisan `(.venv)`

### 2. Install semua library yang dibutuhkan
```bash
pip install -r requirements.txt
```
Ini akan jalan otomatis install semua library yang dibutuhkan, tunggu sampai selesai (5-10 menit tergantung internet).

### 3. Jalankan dashboard!
```bash
streamlit run dashboard/app.py
```
Setelah jalan, browser kamu akan otomatis terbuka di alamat `http://localhost:8501` dan kamu bisa lihat dashboardnya sudah interaktif.

---

## 📚 Daftar Tools &amp; Kegunaannya (Untuk Kamu Tahu Saat Interview Nanti)
| Nama Library | Kegunaan di proyek ini |
|---|---|
| **Pandas** | Tools utama untuk membersihkan data, hitung metrik rasio keketatan, mengolah tabel data — ini skill wajib semua data analyst |
| **Plotly Express** | Membuat grafik interaktif (bisa di-hover, di-filter, di-zoom) jauh lebih menarik untuk portofolio daripada grafik statis Matplotlib |
| **Streamlit** | Membuat website dashboard hanya dengan kode Python saja, tanpa perlu belajar HTML/CSS/frontend. Bisa di-deploy gratis di internet cuma 1 klik. |
| **BeautifulSoup4** | Tools web scraping untuk nanti kamu ambil data dari situs PMB PTN lain (ITS, UNAIR, dll) |
| **NumPy** | Bantuan perhitungan numerik |
| **Geopandas** | Nanti untuk bikin peta persebaran kelulusan per kabupaten Jawa Timur (fitur tambahan) |

---

## 🔗 Daftar Sumber Data Resmi Yang Bisa Kamu Ambil
Semua data ini publik dan boleh kamu ambil untuk proyek, tidak perlu bayar:
1.  Data daya tampung + peminat tiap prodi tiap tahun:
    - Halaman resmi PMB masing-masing PTN (contoh UPN Jatim: https://ppmb.upnjatim.ac.id/jalur-snbp/)
    - Analitica.id: https://analitica.id/tools/daya-tampung-snbp (sudah terkumpul data semua PTN 2021-2026)
2.  Data nama sekolah asal siswa lulus:
    - Pengumuman kelulusan resmi SNPMB: https://pengumuman-snbp.snpmb.id
    - Mirror pengumuman di situs PTN masing-masing
3.  Data akreditasi prodi: https://pddikti.kemdikbud.go.id/
4.  Data akreditasi sekolah: https://ban-sm.kemdikbud.go.id/
5.  Data rekap kelulusan per provinsi: https://snpmb.bppp.kemdikbud.go.id/ (unduh bagian laporan hasil seleksi)

---

## 📝 Rencana Pengerjaan Selanjutnya (Berurutan Jangan Langsung Lompat!)
1.  ✅ Sekarang: Coba jalankan dashboard yang sudah saya buat, pastikan di laptop kamu sudah jalan tidak ada error
2.  Hari 1-2: Tambah data prodi untuk ITS, UNAIR, UB, UM, UNESA tahun 2024-2025 (ambil dari situs PMB masing-masing), masukkan ke file CSV di folder `data/cleaned/`
3.  Hari 3-4: Bersihkan data nama sekolah asal lulusan jika kamu punya data, seragamkan nama yang penulisannya beda
4.  Hari 5-6: Tambah halaman baru di dashboard:
    - Halaman analisis sekolah
    - Halaman rekomendasi prodi
    - Halaman peta Jawa Timur
5.  Hari 7: Buat akun GitHub, upload proyekmu
6.  Hari 8: Deploy dashboard ke Streamlit Cloud (gratis) agar dapat link publik yang bisa kamu taruh di CV/LinkedIn
7.  Hari 9: Tulis 3-5 insight dari data yang kamu dapatkan, buat postingan LinkedIn
