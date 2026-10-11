# Audit versi

Runtime belum dijalankan pada lingkungan pembuatan paket karena Docker tidak tersedia. Isi dokumen ini setelah pemeriksaan di laptop.

| Bukti | Hasil aktual |
|---|---|
| OS laptop | Microsoft Windows 11 Home Single Language (10.0.26200, 64-bit) |
| docker version | Docker Engine 28.5.1 (Docker Desktop 4.49.0), API 1.51, context desktop-linux |
| docker compose version | Docker Compose v2.40.3-desktop.1 |
| docker compose exec odoo odoo --version | Odoo Server 19.0-20260926 |
| check_runtime.py dalam container | Lolos (version matches: 19.0-20260926, all_standard_sources_found: true untuk contacts, stock, purchase, sale_management, mrp, project, purchase_stock, sale_stock) |
| Image Odoo dan digest | odoo:19.0 (ID: 0d96a8dd3e19, digest: sha256:dd9013e669caaa23d26765dc55814655eaeecca7cfc2c265dbabae913bce22fd) |
| Image PostgreSQL dan digest | postgres:16 (ID: 275447c94b11, digest: sha256:ca0bd484cb98bf4b24eb1010e73fb3fcbd6714d240fbc1a10eea5b7dbecb641d) |
| Database tpr_dev | Dibuat melalui web UI, 6 aplikasi standar + 2 modul TPR kustom terpasang aktif |
| Enam aplikasi standar terpasang | contacts, stock, purchase, sale_management, mrp, project aktif di tpr_dev |
| Modul TPR terpasang di tpr_dev | tpr_circular_core, tpr_waste_management terpasang aktif |
| Database tpr_test | Dibuat dari template tpr_dev untuk isolasi uji coba |
| Install tpr_circular_core & tpr_waste_management di tpr_test | Berhasil (Exit Code 0 via CLI entrypoint) |
| Upgrade modul di tpr_test | Berhasil (Exit Code 0 via CLI entrypoint) |
| Uji alur end-to-end (scripts/test_workflow.py) | Lolos 100% (7 assertion steps sukses, Exit Code 0) |

### Catatan Pemeriksaan Runtime (12 Oktober 2026)

1. **Setup Konfigurasi**:
   - `scripts/setup.ps1` berhasil dijalankan.
   - `.env` dan `config/odoo.conf` terbentuk dengan kredensial acak lokal.
   - Filter database `dbfilter = ^tpr_.*$` aktif.

2. **Status Container**:
   - `tpr_odoo19-db-1` (postgres:16): Up (healthy), port 5432/tcp.
   - `tpr_odoo19-odoo-1` (odoo:19.0): Up, port 127.0.0.1:8069->8069/tcp.
   - HTTP service (werkzeug) aktif dan melayani request di port 8069.

3. **Verifikasi Sumber Modul Standar**:
   - Output `python3 /opt/tpr-scripts/check_runtime.py` memastikan seluruh manifest 6 aplikasi standar (`contacts`, `stock`, `purchase`, `sale_management`, `mrp`, `project`) serta bridge modules (`purchase_stock`, `sale_stock`) tersedia di path `/usr/lib/python3/dist-packages/odoo/addons`.
   - Lisensi: LGPL-3.

4. **Audit API & Sintaks Odoo 19 Community**:
   - View Tree telah sepenuhnya digantikan oleh `<list>` (`view_mode = 'list,form'`).
   - RelaxNG Odoo 19 untuk `<search>` tidak memperbolehkan atribut `string` atau `expand` pada tag `<group>` di search view; pengelompokan menggunakan `<filter string="..." name="..." context="{'group_by': '...'}"/>`.
   - Manajemen grup hak akses (`res.groups`) tidak lagi menggunakan `category_id`, melainkan `privilege_id` (`res.groups.privilege`).
   - Atribut `_sql_constraints` lama sudah usang di Odoo 19; constraint model menggunakan `models.Constraint('unique(...)', '...')`.
   - Model `stock.move` tidak lagi memiliki field `name` (menggunakan `description_picking` dan `origin`); field `quantity` dan flag `picked = True` dipakai untuk kuantitas selesai.
   - Model `stock.location` tidak memiliki field `comment`.
   - Field `uom_po_id` berada di `product.template`, bukan `product.product`.
   - Field relasi grup pada user (`res.users`) di Odoo 19 bernama `group_ids` (bukan lagi `groups_id`).
   - Field `shape` (bentuk geometri) dan `measurement_method` (metode timbang fisik vs kalkulasi) diterapkan pada potongan pelat sesuai Bab 8 panduan sistem.
   - Silsilah potongan induk-anak (`parent_piece_id` & `child_piece_ids`) memungkinkan pelacakan turunan sisa pemotongan ulang tanpa memutus asal proyek/MO awal.

5. **Hasil Pengujian Aktual pada tpr_test**:
   - Master data: 3 keluarga material, 3 grade, 8 ketebalan, serta pemetaan produk kesetaraan terpasang.
   - Lokasi fisik sirkular: Karantina Potongan, Rak Reusable, Area Scrap Fisik terbuat.
   - Perhitungan bobot teoretis pelat: dimensi 1000 x 500 x 6 mm baja karbon terhitung 23.55 kg, deviasi berat terhitung otomatis.
   - MO dan By-product: Produksi 100 kg pelat menghasilkan 60 kg barang jadi dan 40 kg by-product potongan ke lokasi karantina (`WH/Stock/Quarantine/Remnants`).
   - Karantina & Otorisasi: Operator tanpa hak manajer ditolak saat approve reuse/scrap; hanya petugas berwenang (Waste Manager) yang dapat memutuskan status.
   - Auto-Suggest Lokasi & Relokasi Stok: Persetujuan reuse otomatis menyarankan lokasi Rak Reusable; penolakan scrap otomatis menyarankan Area Scrap Fisik. Pemindahan memicu `stock.move` resmi dengan lot tracking tanpa memanipulasi `stock.quant` secara langsung.
   - Silsilah Induk-Anak: Potongan anak (strip) yang dipotong dari potongan induk berhasil tercatat, memiliki relasi dua arah (`parent_piece_id` dan `child_piece_ids`), serta mewarisi penelusuran MO awal.
   - Keterlacakan MO: Smart button pada Manufacturing Order menampilkan 3 potongan terkait beserta total berat.
   - Visualisasi MFA Sankey Diagram: Model `tpr.mfa.analysis` terpasang dan teruji, menghasilkan diagram aliran massa (Sankey SVG responsif) interaktif yang memetakan masukan baru/ulang, pemotongan fabrikasi, produk jadi, remnant reusable, scrap fisik, kerf loss, dan loop sirkularitas.

6. **Keterangan Keamanan**:
   - Tidak ada master password, database password, atau kredensial pengguna yang dicatat dalam dokumen ini.
