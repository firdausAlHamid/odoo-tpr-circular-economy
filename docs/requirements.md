# Kebutuhan awal penelitian

## Posisi pekerjaan

Daus mengusulkan Waste Management dan MFA untuk sisa pelat CV Teknika Prima Raya. Rancangan integrasi disusun Daus terlebih dahulu. Peran Manufacturing Feriangga masih perlu dibahas dan disepakati.

## Lingkup pertama

- Satu database pengembangan tpr_dev dan database pengujian tpr_test bila diperlukan.
- Satu perusahaan, satu gudang, satu keluarga pelat, dan satu alur fabrikasi terpilih untuk prototipe awal.
- Enam aplikasi standar: Contacts, Inventory, Purchase, Sales, Manufacturing, Project.
- Dua fokus penelitian dan dua dashboard yang direncanakan. Empat paket addon adalah susunan kode, bukan empat TA.
- Ukuran dalam mm sebagai metadata dan massa dalam kg sebagai satuan stok untuk keluarga pelat. Jenis material dan periode lapangan perlu dikonfirmasi.

## Alur inti

Produksi mencatat konsumsi dan keluaran. Remnant serta scrap yang masih disimpan dicatat sebagai by-product fisik. Waste Management menambahkan identitas, pemeriksaan, lokasi, riwayat reuse, penyaluran, serta laporan MFA. Reuse menghubungkan MO asal dengan MO tujuan. Jumlah stok bersumber dari transaksi standar yang selesai.

## Batas kontribusi awal

| Area | Kontribusi yang diusulkan |
|---|---|
| Daus | Pengelolaan potongan inspeksi stok reuse dispatch MFA dashboard Waste |
| Feriangga | Manufacturing pemakaian bahan dan indikator produksi untuk dibahas bersama |
| Bersama | Definisi material kontrak data setup dan pengujian integrasi |

Data simulasi digunakan untuk uji perangkat lunak. Klaim manfaat perusahaan memerlukan data lapangan dan evaluasi yang mendukung. Kelayakan pemakaian material diputuskan petugas perusahaan, sedangkan sistem mencatat dan membantu menelusuri keputusan.
