# Aturan kerja proyek

- Gunakan Odoo 19 Community dan periksa source runtime sebelum memakai API atau sintaks view.
- Baca README.md, docs/requirements.md, dan version_audit.md sebelum perubahan.
- Tahap awal harus membuat Odoo berjalan dan aplikasi standar tersedia sebelum fitur penelitian.
- Semua addon khusus berada di addons. Addon pihak ketiga berada di third_party_addons dengan folder modul dipertahankan.
- Gunakan fitur standar jika memenuhi kebutuhan. Jangan mengubah source core Odoo.
- Saldo material fisik berasal dari transaksi stock standar yang selesai. Form analisis tidak menulis saldo stock.quant sendiri.
- Pembagian Manufacturing dengan Feriangga masih usulan sampai dicatat sebagai keputusan bersama.
- Data simulasi dan data perusahaan dibedakan. Jangan mengarang wawancara, pengukuran, atau manfaat perusahaan.
- Simpan bukti pemeriksaan versi, install, upgrade, fungsi, dan hitungan. Jangan menulis test pass tanpa menjalankannya.
- Password lokal tidak masuk Git, prompt, atau ringkasan hasil. Setup mempertahankan konfigurasi yang sudah ada.
- Gunakan database tpr_test untuk pengujian yang mengubah data. Pertahankan database dan volume yang ada.
