# Mulai Proyek Odoo 19 TPR di Antigravity

Bro, target awalnya Odoo 19 Community bisa dibuka di laptop dan aplikasi standar bisa digunakan. Download wajib dari Odoo Apps Store untuk tahap ini adalah **nol**. Compose akan mengambil image Odoo dan PostgreSQL. Aplikasi standar ada di distribusi Odoo, lalu diaktifkan pada database lokal.

Paket ini menyediakan lingkungan awal dan prompt. Modul Waste Management, MFA, dan dashboard penelitian belum diimplementasikan. Folder addon khusus disediakan untuk pengembangan berikutnya. Pembagian dengan Feriangga masih usulan yang perlu disepakati.

## 1 Instal alat

- Instal Docker Desktop untuk sistem operasi lu, lalu jalankan sampai engine aktif. Pada Windows gunakan backend WSL 2 dan Linux containers.
- Instal Antigravity IDE, lakukan login sesuai panduan resminya.
- Git bisa ditambahkan saat mulai menyimpan riwayat kode. Odoo dan PostgreSQL tidak perlu dipasang lagi sebagai aplikasi terpisah untuk jalur Docker ini.

Link resmi:

- Docker Desktop: https://docs.docker.com/desktop/setup/install/
- Antigravity: https://antigravity.google/download/
- Panduan Antigravity IDE: https://codelabs.developers.google.com/getting-started-agy-ide

## 2 Ekstrak dan buka folder

Ekstrak ZIP. Buka folder **tpr-odoo19** di Antigravity melalui Open Folder. Pilih folder yang langsung berisi compose.yaml dan README.md.

| Path | Fungsi |
|---|---|
| compose.yaml | Menjalankan Odoo dan PostgreSQL |
| .env.example | Template pengaturan lokal |
| config/odoo.conf.example | Template konfigurasi Odoo |
| addons/ | Kode addon penelitian |
| third_party_addons/ | Addon pihak ketiga yang sudah diperiksa |
| scripts/ | Setup dan pemeriksaan sumber Odoo |
| prompts/ | Prompt untuk Antigravity per tahap |
| docs/ | Rancangan, pemeriksaan versi, dan bukti pekerjaan |

## 3 Siapkan konfigurasi

Buka terminal dari Antigravity di folder tpr-odoo19. Pilih salah satu sesuai OS.

Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

macOS atau Linux dengan Python 3:

```bash
python3 scripts/setup.py
```

Kalau Python 3 belum tersedia, Antigravity dapat memakai container sementara berikut melalui Docker. Command ini bisa digunakan juga pada Windows:

```text
docker run --rm --mount "type=bind,source=.,target=/work" -w /work python:3.12-alpine python scripts/setup.py
```

Setup membuat .env dan config/odoo.conf dengan password baru. Menjalankannya lagi tidak mengganti konfigurasi yang sudah lengkap.

Alternatif manual: salin .env.example menjadi .env dan config/odoo.conf.example menjadi config/odoo.conf. Ganti masing-masing penanda CHANGE_ME dengan password pilihan lu. Jangan campur konfigurasi dari proyek lain.

## 4 Jalankan Odoo

```text
docker version
docker compose version
docker compose up -d
docker compose ps
docker compose exec odoo odoo --version
```

Saat pertama kali dijalankan, Docker mengunduh image Odoo 19 dan PostgreSQL 16. Tunggu sampai db berstatus healthy dan odoo berjalan. Buka http://localhost:8069 atau langsung http://localhost:8069/web/database/manager.

Gunakan tag odoo:19.0. Tag latest dapat menunjuk versi utama lain. Untuk laporan penelitian, catat versi dan digest image yang benar-benar digunakan.

## 5 Buat database pertama

- Master Password: nilai admin_passwd dari config/odoo.conf.
- Database Name: **tpr_dev**. Nama database perlu diawali tpr_ sesuai filter paket ini.
- Email: akun admin lokal yang lu tentukan.
- Password: password login admin Odoo yang lu tentukan sendiri.
- Country: Indonesia.
- Language: pilih yang lu gunakan, misalnya English agar cocok dengan nama menu panduan.
- Demo Data: jangan centang agar data latihan penelitian lebih mudah dikendalikan.
- Timezone pada profil pengguna: Asia/Jakarta.

| Jenis password | Kegunaan |
|---|---|
| POSTGRES_PASSWORD dalam .env | Koneksi server Odoo ke PostgreSQL |
| admin_passwd dalam config/odoo.conf | Membuat dan mengelola database Odoo |
| Password akun admin | Login ke aplikasi Odoo |

Ketiganya mempunyai fungsi berbeda. Lu memakai master password saat membuat database dan password akun admin saat login.

## 6 Aktifkan enam aplikasi standar

Masuk menu Apps pada Odoo lokal, cari aplikasi berikut lalu gunakan Install atau Activate sesuai tombol yang tersedia.

| Aplikasi | Nama teknis | Fungsi awal |
|---|---|---|
| Contacts | contacts | Supplier pembeli dan pelanggan |
| Inventory | stock | Stok lokasi penerimaan dan pengeluaran |
| Purchase | purchase | Pembelian bahan |
| Sales | sale_management | Penjualan termasuk penyaluran scrap |
| Manufacturing | mrp | BoM MO konsumsi dan by-product |
| Project | project | Daftar proyek atau pekerjaan |

Dependency standar akan dipasang sesuai kebutuhan. Jumlah addon teknis yang ikut terpasang bisa lebih dari enam. purchase_stock dan sale_stock menjadi penghubung transaksi pembelian atau penjualan dengan stok. Mereka tidak dihitung sebagai fokus penelitian tambahan.

Hubungan Project dengan MO untuk kebutuhan TA perlu dianalisis dan dilengkapi dalam addon sendiri. Pengaktifan enam aplikasi belum membentuk modul Waste Management penelitian.

Periksa sumber standar melalui:

```text
docker compose exec odoo python3 /opt/tpr-scripts/check_runtime.py
```

Script memeriksa versi serta keberadaan manifest, bukan status instalasi dalam database.

## 7 Kirim prompt pertama

Buka prompts/01_setup_antigravity.txt dan salin isinya ke panel agent Antigravity. Prompt itu meminta pemeriksaan lingkungan, startup, dan bukti versi. Kalau lu sudah menyelesaikan langkah manual, agent melanjutkan dari keadaan yang ada.

Sesudah Odoo dan aplikasi standar siap, gunakan prompts/02_core_dan_waste.txt. Prioritaskan data material dan pencatatan sisa yang kecil tetapi bisa diuji. prompts/03_integrasi_dan_dashboard.txt dipakai setelah alur transaksi sudah berjalan dan batas integrasi sudah dibahas.

## 8 Kalau nanti mengunduh addon dari Apps Store

Untuk awal belum ada addon pihak ketiga yang diwajibkan. Kalau nanti ada kebutuhan yang jelas, periksa versi 19.0, kompatibilitas Community, lisensi, dan dependencies pada __manifest__.py. Addon gratis bisa tetap memiliki dependency tambahan atau kebutuhan Python yang belum tersedia.

Ekstrak setiap ZIP dan pertahankan folder masing-masing modul. Lokasi manifest harus seperti **third_party_addons/nama_modul/__manifest__.py**. Jangan menumpuk semua file modul dalam satu folder karena nama file seperti __init__.py dan __manifest__.py akan bertabrakan.

Kalau ZIP berisi satu repository dengan banyak addon, ambil folder modul yang diperlukan beserta dependency addonnya. Alternatifnya, tambahkan root repository itu sebagai addons_path tersendiri. Konfigurasi paket ini membaca folder addon langsung di third_party_addons dan addons.

Sesudah menambahkan addon:

```text
docker compose restart odoo
```

Aktifkan developer mode dari Settings atau buka URL Odoo dengan ?debug=1. Masuk Apps lalu Update Apps List. Hapus filter Apps bila modul tidak berstatus aplikasi. Cari nama teknis addon dan instal setelah dependencies tersedia.

Untuk memperbarui modul yang sudah terpasang, restart untuk memuat kode Python dan lakukan upgrade modul untuk perubahan model, field, XML, atau security. Update Apps List hanya menyegarkan daftar modul.

## 9 Command sehari-hari

```text
docker compose up -d
docker compose ps
docker compose logs --tail=100 odoo
docker compose restart odoo
docker compose stop
```

Volume bernama mempertahankan database dan filestore ketika service berhenti. Simpan backup sebelum perubahan besar. Command down dengan opsi -v menghapus volume data dan bukan langkah rutin paket ini.

## 10 Target sesi pertama

- Odoo terbuka di localhost:8069.
- Versi Odoo sesuai 19.
- Database tpr_dev dibuat dan login berhasil.
- Enam aplikasi standar aktif.
- Bisa membuat satu produk bahan latihan serta satu BoM dan MO sederhana.
- Belum mengklaim modul Waste Management atau integrasi penelitian sudah selesai.

## Rujukan

- Image resmi Odoo dan custom addon mount: https://hub.docker.com/_/odoo
- Entrypoint image Odoo 19: https://github.com/odoo/docker/blob/master/19.0/entrypoint.sh
- Kode Community 19: https://github.com/odoo/odoo/tree/19.0
- Instalasi aplikasi: https://www.odoo.com/documentation/19.0/applications/general/apps_modules.html
- By-products: https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/manufacturing/workflows/byproducts.html
- CLI dan addons path: https://www.odoo.com/documentation/19.0/developer/reference/cli.html
- Google Antigravity IDE: https://codelabs.developers.google.com/getting-started-agy-ide

Docker tidak tersedia pada lingkungan penyusunan paket ini. Konfigurasi dan script setup Python diperiksa secara lokal. Startup image, instalasi aplikasi, script runtime dalam container, dan script PowerShell perlu diverifikasi di laptop lu melalui langkah di atas.
