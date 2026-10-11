# **Panduan Pengembangan Sistem Odoo 19 untuk Produksi dan Pengelolaan Sisa Pelat** 

_CV Teknika Prima Raya_ 

_Firdaus Al Hamid dan Feriangga_ 

_Spesifikasi sistem dan prompt implementasi Antigravity_ 

_11 Oktober 2026_ 

Sistem yang dirancang menghubungkan kebutuhan bahan untuk suatu proyek, pemakaian bahan di produksi, pembentukan sisa pelat, penyimpanan potongan, pemakaian ulang, dan penjualan scrap dalam satu database Odoo 19 Community. Feriangga mengembangkan pengendalian produksi dan indikator efisiensi penggunaan material. Firdaus mengembangkan pengelolaan sisa material dan Material Flow Analysis atau MFA. Hubungan keduanya memungkinkan satu potongan ditelusuri dari proyek asal sampai pemanfaatannya pada pekerjaan berikutnya. 

Panduan ini menjelaskan rancangan yang harus diwujudkan, urutan pengerjaan, struktur data, aturan transaksi, dashboard, contoh perhitungan, pengujian, dan dokumentasi penelitian. Bagian 17 berisi prompt lengkap yang dapat disalin ke Antigravity. Bagian 18 berisi instruksi lanjutan untuk setiap tahap pembangunan. Bagian 19 menghubungkan pekerjaan sistem dengan bukti yang diperlukan untuk laporan Tugas Akhir. 

Keputusan dasar adalah menggunakan modul standar gratis sebagai fondasi, kemudian menambah modul khusus untuk kebutuhan potongan pelat dan indikator penelitian. Prototype yang berhasil secara teknis tetap perlu divalidasi terhadap proses, ukuran material, dan kebutuhan pengguna perusahaan. 

1 

## **Isi panduan** 

- 1 Konteks perusahaan dan sasaran sistem 

2 Pemisahan kontribusi kedua Tugas Akhir 

- 3 Ruang lingkup yang dapat diselesaikan 

4 Platform dan modul yang digunakan 

- 5 Arsitektur integrasi dan pemilik data 

- 6 Alur operasional dari awal sampai akhir 

- 7 Representasi material dan lokasi 

- 8 Model data yang harus dibangun 

- 9 Aturan transaksi dan validasi 

- 10 MFA dan rumus indikator 

- 11 Dashboard dan kebutuhan tampilan 

- 12 Peran pengguna dan pengendalian akses 

- 13 Lingkungan pengembangan dan struktur repository 

- 14 Urutan pembangunan dan kriteria selesai 

15 Data demonstrasi dan perhitungan acuan 

- 16 Pengujian dan kriteria penerimaan 

- 17 Prompt lengkap untuk Antigravity 

- 18 Prompt lanjutan per tahap 

- 19 Menghubungkan sistem dengan laporan penelitian 

- 20 Rujukan dan sumber teknis 

2 

## **1 Konteks perusahaan dan sasaran sistem** 

### **1.1 Masalah yang menjadi dasar rancangan** 

Profil CV Teknika Prima Raya menunjukkan kegiatan manufaktur refraktori, fabrikasi, konstruksi, instalasi, dan perbaikan. Produk dan bahan yang dicantumkan meliputi anchor refractory, steel support, steel fibre, serta material SS304, SS310, SS316, dan MS atau CS. Profil juga memperlihatkan hubungan pesanan pelanggan, gambar, penyiapan, produksi, pemeriksaan, pengemasan, dan pengiriman. Variasi spesifikasi ini menjadi alasan pencatatan bahan tidak cukup hanya menggunakan nama umum seperti besi atau pelat (CV Teknika Prima Raya, tanpa tahun, hlm. 1, 8, dan 19). 

Informasi awal dalam draf Firdaus menggambarkan pengerjaan proyek, termasuk unit mixer, yang menghasilkan potongan pelat. Sebagian potongan masih berpotensi digunakan, sebagian dijual menurut berat, dan pengetahuan mengenai keberadaannya bergantung pada orang tertentu. Rancangan diarahkan agar pengguna dapat menjawab pertanyaan operasional yang konkret: potongan apa yang tersedia, di mana letaknya, apakah sesuai dengan kebutuhan pekerjaan, berasal dari proyek mana, dan apa tindak lanjutnya. 

Hubungan penumpukan material dengan kesulitan pendanaan yang disebutkan dalam draf merupakan indikasi untuk diperiksa. Sistem menyediakan informasi stok dan transaksi penjualan yang dapat membantu pemeriksaan itu. Kesimpulan mengenai kerugian, modal tertahan, atau penyebab masalah kas memerlukan dokumen biaya dan arus kas tersendiri. 

### **1.2 Sasaran keberhasilan** 

- Pengguna dapat menemukan potongan berdasarkan grade, ketebalan, ukuran, kondisi, dan lokasi tanpa mengandalkan ingatan satu orang. 

- Setiap perintah produksi memiliki rencana bahan, pemakaian aktual, keluaran material terpilih, sisa yang dapat digunakan, scrap fisik, dan catatan selisih neraca massa. 

- Pemakaian ulang mengurangi stok potongan asal dan mempunyai hubungan yang jelas dengan produksi tujuan. 

- Penjualan scrap mengurangi stok ketika material benar-benar diserahkan. Nilai penjualan dan penerimaan uang ditampilkan dengan pengertian yang berbeda. 

- Dashboard dapat ditelusuri ke transaksi sumber dan menghasilkan angka yang sama dengan perhitungan manual pada data acuan. 

### **1.3 Fakta dan keputusan yang perlu dikonfirmasi** 

|**Hal**|**Dasar saat ini**|**Bukti yang dibutuhkan**|
|---|---|---|
|Produk dan<br>spesifikasi bahan|Profil perusahaan|Daftar bahan yang benar-benar dipakai pada<br>proyek terpilih|
|Sisa pelat dan<br>penjualan menurut<br>berat|Informasi awal pada draf Firdaus|Wawancara penanggung jawab, pemeriksaan<br>fisik, nota timbang dan penjualan|
|Cara pencatatan|Indikasi ketergantungan pada orang|Observasi alur pencarian dan dokumen|
|dan pencarian stok|tertentu|pencatatan yang tersedia|



3 

|**Hal**|**Dasar saat ini**|**Bukti yang dibutuhkan**|
|---|---|---|
|Status UMKM|Frasa dalam judul penelitian|Konfirmasi klasifikasi skala usaha dari data<br>perusahaan|
|Proses penelitian|Usulan fabrikasi pelat|Proyek atau komponen yang bisa diikuti dari<br>masukan sampai keluaran|
|Periode<br>pengamatan|Belum ditetapkan|Tanggal awal dan akhir, stok awal, stok akhir,<br>dan barang dalam proses|
|Kelayakan<br>pemakaian ulang|Keputusan teknis perusahaan|Kriteria grade, ukuran, ketebalan, kondisi,<br>dan pihak yang menyetujui|



## **2 Pemisahan kontribusi kedua Tugas Akhir** 

Kedua penelitian menggunakan platform dan data bersama, tetapi mempunyai pertanyaan, artefak, dan evaluasi masing-masing. Pemisahan ini dicantumkan dalam analisis kebutuhan, log pengembangan, laporan pengujian, dan penjelasan pada sidang. 

|**Aspek**|**Firdaus Al Hamid**|**Feriangga**|
|---|---|---|
|Fokus masalah|Informasi, penelusuran, dan tindak lanjut<br>sisa pelat|Perbandingan kebutuhan bahan dengan<br>pemakaian serta keluaran produksi|
|Artefak utama|Modul Waste Management dan<br>dashboard MFA|Pengembangan Manufacturing dan<br>dashboard efisiensi material|
|Unit analisis|Potongan, stok gudang sisa, dan aliran<br>antarproyek|Perintah produksi atau pekerjaan yang<br>menghasilkan komponen terpilih|
|Indikator utama|Stok sisa, umur stok, massa dipakai ulang,<br>penyaluran, selisih neraca|Yield material, deviasi terhadap rencana,<br>komposisi keluaran, proporsi bahan ulang|
|Kepemilikan logika|Identitas potongan, klasifikasi,<br>pemanfaatan, penyaluran, laporan MFA|Rencana dan aktual bahan, keluaran<br>produksi, pemeriksaan kelengkapan neraca|
|Pengujian mandiri|Traceability, rekonsiliasi sisa, transaksi<br>penjualan dan pemakaian ulang|Konsumsi bahan, validasi neraca per<br>produksi, rumus efisiensi|
|Integrasi bersama|Menerima identitas sisa dari hasil<br>produksi|Menerima kandidat potongan dan<br>memasukkannya ke konsumsi produksi<br>tujuan|



Konsep Circular Economy diterjemahkan menjadi kemampuan operasional untuk mempertahankan kegunaan material. Sistem mendukung pencarian dan penggunaan kembali potongan, pemeriksaan kebutuhan bahan, serta pencatatan penyaluran scrap. Penjualan kepada pengepul merupakan penyaluran material. Status telah didaur ulang hanya diberikan apabila ada bukti proses dari pihak penerima. 

4 

## **3 Ruang lingkup yang dapat diselesaikan** 

### **3.1 Minimum viable product** 

MVP mencakup satu perusahaan, satu gudang, beberapa lokasi internal, pengguna dengan peran berbeda, dan satu keluarga proses fabrikasi pelat. Produk akhir boleh berbeda, tetapi neraca hanya menghitung keluarga material terpilih. Misalnya penelitian memilih pelat MS dengan beberapa ketebalan, sementara baut atau cat pada assembly berada di luar neraca pelat. 

Fitur wajib meliputi master material, referensi proyek, BoM dan manufacturing order atau MO, konsumsi aktual, pencatatan keluaran material terpilih, by-product berupa remnant dan scrap fisik, identitas potongan, reservasi pemakaian ulang, penjualan scrap, MFA, dua dashboard, ekspor CSV, dan jejak perubahan. 

### **3.2 Fitur tambahan setelah MVP stabil** 

Label QR, kandidat potongan dengan urutan rekomendasi, ekspor XLSX, impor catatan historis, pengingat umur stok, dan dashboard OWL yang lebih interaktif dapat ditambahkan setelah angka dasar konsisten. Label QR membuka catatan potongan bagi pengguna yang sudah login. Pencarian kandidat merupakan alat bantu dengan kriteria eksplisit, bukan jaminan bahwa material layak secara teknik. 

### **3.3 Cakupan yang tidak dijadikan syarat MVP** 

Optimasi nesting atau pola pemotongan, simulasi CAD, sensor timbangan otomatis, optimasi jadwal mesin, perhitungan emisi daur hidup, akuntansi biaya lengkap, dan pengendalian arus kas berada di luar sasaran awal. Integrasi pajak dan akuntansi mengikuti kebutuhan perusahaan setelah prototipe operasional berhasil. Pembatasan ini menjaga keterukuran kontribusi dua penelitian. 

## **4 Platform dan modul yang digunakan** 

### **4.1 Pilihan platform** 

Gunakan Odoo 19.0 Community yang dipasang secara lokal dengan Docker atau pada server yang dikelola sendiri. Addon Python khusus memerlukan lingkungan yang memperbolehkan pemasangan kode server. Lingkungan lokal dipilih untuk prototipe, pengujian, dan demonstrasi. Antigravity digunakan sebagai IDE dan agen pengembangan, sedangkan Odoo menjalankan aplikasi bisnisnya. 

Dokumentasi dan kode cabang 19.0 menunjukkan dukungan manufacturing order serta by-product. Fitur itu menjadi fondasi pencatatan keluaran produksi. Kebutuhan identitas potongan, neraca penelitian, dan dashboard khusus tetap memerlukan pengembangan tersendiri (Odoo, dokumentasi 19.0 dan kode sumber cabang 19.0). 

### **4.2 Modul standar dan pengembangan khusus** 

|**Modul teknis**|**Penggunaan dalam sistem**|**Keputusan**|
|---|---|---|
|contacts|Pemasok, pelanggan proyek, dan<br>pembeli scrap|Gunakan standar|



5 

|**Modul teknis**|**Penggunaan dalam sistem**|**Keputusan**|
|---|---|---|
|stock|Produk, lot, lokasi, penerimaan,<br>transfer, dan pengiriman|Fondasi stok wajib|
|purchase dan purchase_stock|Pesanan pembelian dan penerimaan<br>bahan|Gunakan untuk alur pembelian<br>sederhana|
|sale_management dan<br>sale_stock|Penjualan proyek atau scrap dan<br>delivery|Gunakan untuk bukti komersial dan<br>keluarnya stok|
|mrp|BoM, MO, bahan aktual, hasil<br>produksi, dan by-product|Fondasi Manufacturing wajib|
|project|Referensi proyek dan pekerjaan|Gunakan project.project, tambah<br>hubungan ke MO|
|mail dan web|Chatter, kegiatan, serta tampilan<br>backend|Dependensi pendukung|
|tpr_circular_core|Keluarga material, definisi ukuran,<br>kebijakan, dan ledger kejadian|Dikembangkan bersama|
|tpr_manufacturing_ce|Rencana bahan, keluaran massa,<br>yield, dan validasi MO|Artefak Feriangga|
|tpr_waste_management|Potongan, klasifikasi, pencarian,<br>pemakaian ulang, penyaluran|Artefak Firdaus|
|tpr_circular_dashboard|Dua dashboard dan laporan<br>berdasarkan sumber yang sama|Tampilan bersama, indikator<br>dibedakan|



Hubungan standar Project dan Manufacturing tidak diasumsikan otomatis tersedia dalam Community. Tambahkan field project_id dan hubungan balik yang diperlukan pada addon sendiri. Accounting bukan dependensi wajib MVP. Jika faktur dan pembayaran diperlukan, buat integrasi tambahan terpisah yang hanya dipasang setelah konfigurasi akuntansi ditetapkan. 

### **4.3 Addon gratis yang dapat dipertimbangkan** 

|**Addon**|**Sumber dan versi yang ditemukan**|**Penggunaan dan pemeriksaan**|
|---|---|---|
|web_responsive|OCA web, cabang 19.0, daftar modul<br>19.0.1.1.0|Opsional untuk navigasi backend. Periksa<br>manifest dan dependensi, lalu uji di database<br>terpisah|
|stock_no_negative|OCA stock logistics workflow, versi<br>19.0.1.0.0, AGPL-3|Opsional untuk kebijakan stok negatif. Uji<br>penerimaan, by-product, retur, dan konsumsi<br>MO|



Ketersediaan versi diperiksa dari listing pengelola pada 11 Oktober 2026. Rekomendasi ini bukan bukti addon sudah diuji dengan modul khusus. Simpan commit, manifest, dependensi, dan lisensi setiap addon yang 

6 

akhirnya dipasang. Harga nol tidak otomatis berarti izin penggunaan tanpa syarat. Jika addon berlisensi AGPL-3 digunakan, ikuti ketentuan lisensinya dalam distribusi hasil penelitian. 

Dashboard MVP dibuat menggunakan model laporan, list, graph, dan pivot Odoo. Kartu KPI khusus dapat dibuat dengan OWL. Dengan demikian kebutuhan dashboard tidak bergantung pada pembelian addon marketplace. Addon pihak ketiga untuk tampilan hanya ditambahkan jika fungsi inti dan angka laporan sudah benar. 

## **5 Arsitektur integrasi dan pemilik data** 



<!-- Start of picture text -->
Pembelian dan penerimaan Manufacturing Komponen jadi<br>bahan baru rencana dan aktual bahan dan produk<br>won “~,x<br>aliran potonganWaste Managementdan inspeksi disimpanScrapdalam fisik stok<br>internal<br>Pemakaian ulang Penjualan atau disposal<br>ke produksi berikutnya dengan dokumen stok<br><!-- End of picture text -->

Alur utama adalah pesanan atau proyek menjadi kebutuhan bahan, kemudian MO mencatat bahan yang diproses. Hasil MO menghasilkan produk, potongan yang masih bisa dipakai, scrap fisik, dan kehilangan proses yang diukur atau diperkirakan. Potongan yang tersedia dapat menjadi bahan pada MO berikutnya. Scrap yang dijual keluar melalui delivery standar. Kedua dashboard membaca transaksi yang sama dari sudut penelitian masing-masing. 

**Pemilik kuantitas persediaan adalah stock.move dan stock.move.line berstatus done, dengan stock.quant sebagai keadaan stok saat ini.** Form khusus tidak boleh langsung menulis quantity atau reserved_quantity pada quant. Ledger material menyediakan identitas kejadian dan klasifikasi analitis, kemudian merujuk ke dokumen stok atau MO yang sudah disahkan. 

**Pemilik jumlah komersial adalah dokumen penjualan dan bukti transaksi.** Nilai sale order yang dikonfirmasi tidak disamakan dengan uang yang diterima. Bila akuntansi belum dipasang, catatan penerimaan uang bersifat catatan operasional yang memerlukan bukti dan rekonsiliasi. 

**Pemilik keputusan kelayakan adalah penanggung jawab teknis perusahaan.** Sistem menyimpan kriteria dan persetujuannya. Kelengkapan ukuran atau hasil pencarian otomatis tidak menggantikan pemeriksaan kondisi material. 

7 

Dependensi addon harus satu arah. Core tidak bergantung pada Manufacturing CE atau Waste Management. Kedua addon tersebut bergantung pada core dan modul standar yang dipakai. Dashboard boleh bergantung pada keduanya. Fungsi serah terima ditempatkan pada core atau extension yang tidak membuat kedua addon saling mengimpor. 

## **6 Alur operasional dari awal sampai akhir** 

### **6.1 Persiapan dan penerimaan bahan** 

1. Administrator menyiapkan company, pengguna, satuan, kategori produk, keluarga material, dan lokasi. 

2. Petugas mencatat proyek dan produk atau komponen yang akan dibuat. Gambar dan revisi kebutuhan bahan dapat dilampirkan. 

3. Planner membuat BoM dan rencana bahan. Petugas memeriksa stok baru serta kandidat potongan yang sesuai sebelum mengusulkan pembelian. 

4. Bahan baru diterima melalui receipt standar. Grade, ketebalan, sumber, dan identitas lot harus sesuai keluarga material. Pelat yang perlu ditelusuri per benda menggunakan satu lot untuk satu benda fisik, dengan kuantitas dalam kg. 

### **6.2 Produksi dan pencatatan sisa** 

5. Planner membuat MO untuk proyek. Rencana bahan disimpan sebagai baseline, termasuk tanggal dan alasan revisi. 

6. Bahan yang benar-benar diproses dipilih berdasarkan lot. Penerbitan reservasi atau transfer internal belum menjadi konsumsi akhir. 

7. Operator mengisi konsumsi aktual dan massa material terpilih yang masuk ke produk atau komponen. Untuk assembly, timbang atau estimasikan hanya massa keluarga pelat yang sedang dianalisis. 

8. Operator mencatat sisa yang dapat digunakan kembali, scrap yang masih disimpan, dan kehilangan proses. Tiap potongan memiliki identitas serta ukuran. Keluaran remnant dan scrap yang disimpan menggunakan by-product stok. 

9. Supervisor memeriksa kelengkapan serta selisih neraca. Sesudah MO benar-benar selesai, addon membuat catatan potongan dan kejadian dengan merujuk ke move by-product yang sudah done. Jika selesai sebagian, pencatatan mengikuti bagian yang benar-benar diposting dan hubungan backorder. 

### **6.3 Pemeriksaan dan penyimpanan** 

10. Potongan masuk ke lokasi karantina. Petugas teknis menentukan reusable, scrap untuk penyaluran, atau perlu pemeriksaan tambahan. Lokasi internal dan catatan kondisi disesuaikan. 

11. Klasifikasi yang mengubah kelompok produk, misalnya remnant menjadi scrap, menggunakan transaksi konversi terkendali dengan input dan output setara massa. Perubahan field status saja tidak boleh menyisakan kuantitas pada produk lama sekaligus menambah produk baru. 

8 

### **6.4 Pemakaian ulang dan penyaluran** 

12. Planner mencari potongan berdasarkan keluarga material, ketebalan, ukuran, kondisi, dan lokasi. Supervisor mengesahkan kecocokan terhadap kebutuhan pekerjaan. 

13. Wizard pemakaian ulang menautkan potongan ke MO tujuan, menyiapkan substitusi komponen yang setara, dan memesan stock move melalui mekanisme standar. Klik reservasi belum menambah KPI massa dipakai ulang. 

14. Saat pemotongan dilakukan, benda induk dikonsumsi penuh. Jika masih ada sisa fisik, sisa itu menjadi potongan anak dengan lot baru dan parent_piece_id. Dengan cara ini ukuran induk tidak dibiarkan seolah masih utuh setelah dipotong. 

15. Scrap dapat dijual melalui sale order dan delivery. Delivery done mengurangi stok. Bukti timbang, identitas pembeli, harga, dan penerimaan uang dicatat pada data operasional yang terhubung. 

16. Material yang benar-benar dibuang keluar melalui transaksi yang sesuai, termasuk stock.scrap untuk barang yang masih berada di stok. Kehilangan potong yang sudah termasuk konsumsi MO tidak dikurangi lagi melalui scrap tambahan. 

## **7 Representasi material dan lokasi** 

### **7.1 Produk dan satuan** 

Gunakan keluarga material sebagai penghubung spesifikasi yang setara. Contoh keluarga adalah pelat MS 3 mm. Di dalamnya terdapat produk bahan baru PLT_MS_3, produk potongan REM_MS_3, dan produk scrap SCR_MS_3. Jika scrap digabung antarketebalan, kelompok grade harus tetap terpisah dan aturan pelacakan asal dijelaskan. 

Ketiga produk stok menggunakan satuan massa kg. Dimensi panjang, lebar, dan ketebalan disimpan sebagai metadata dalam mm. Jumlah potongan berasal dari identitas benda fisik, bukan konversi tetap antara unit dan kg. Produk hasil dapat menggunakan unit, dengan massa material terpilih disimpan pada catatan keluaran MO. 

Contoh kode potongan adalah REM-2026-00001. Kode lot dipakai sebagai identitas stok. Satu remnant yang perlu ditelusuri merupakan satu lot untuk satu benda fisik. Tracking menggunakan lot, karena benda mempunyai massa yang tidak selalu satu kg. Scrap yang dikumpulkan dapat memakai satu lot untuk satu batch penimbangan. 

BoM menggunakan produk bahan baru sebagai rencana. Jika remnant dipilih, addon menambahkan atau mengganti baris konsumsi dengan produk remnant setara berdasarkan persetujuan planner, sambil mempertahankan baseline. Penggantian tidak boleh menambah konsumsi dua kali atau membiarkan baris bahan baru tetap dikonsumsi penuh untuk kebutuhan yang telah dipenuhi remnant. 

### **7.2 Lokasi stok** 

|**Lokasi**|**Jenis**|**Fungsi**|
|---|---|---|
|WH Bahan Baru|Internal|Pelat baru yang tersedia|



9 

|**Lokasi**|**Jenis**|**Fungsi**|
|---|---|---|
|WH Karantina Sisa|Internal|Potongan yang menunggu pemeriksaan|
|WH Sisa Layak|Internal|Potongan yang disetujui untuk pemakaian<br>ulang|
|WH Scrap Siap<br>Salur|Internal|Scrap fisik yang masih dimiliki perusahaan|
|Production|Lokasi produksi standar|Transformasi masukan menjadi keluaran MO|
|Customers|Eksternal standar|Tujuan material yang sudah diserahkan<br>kepada pembeli|
|Scrap atau<br>Disposal|Lokasi virtual standar|Barang yang benar-benar keluar dari<br>inventaris untuk dibuang|



Lokasi karantina, remnant, dan scrap siap salur harus terpisah dari jalur reservasi bahan baru secara otomatis. Reservasi potongan dilakukan melalui wizard setelah pemeriksaan. Status belum diperiksa mencegah konsumsi ke proyek berikutnya. 

### **7.3 Pengukuran dan ketidakpastian** 

Penimbangan aktual diutamakan. Apabila suatu pelat berbentuk persegi panjang belum ditimbang, perkiraan massa dapat dihitung dari panjang dalam meter dikali lebar dalam meter dikali ketebalan dalam meter dikali massa jenis dalam kg per meter kubik. Massa jenis disimpan dengan sumber dan tanggal, sesuai grade material. Jangan menggunakan satu massa jenis untuk semua grade tanpa dasar. 

Simpan measurement_method, measured_at, measured_by, alat, ketelitian, density_source, dan catatan bentuk. Perkiraan dari persegi pembatas potongan tidak beraturan tidak boleh diberi label pengukuran aktual. Potongan tersebut perlu ditimbang atau mempunyai luas efektif dari sumber yang dapat dipertanggungjawabkan. 

## **8 Model data yang harus dibangun** 

Nama teknis berikut merupakan kontrak rancangan addon sendiri. Field standar Odoo harus diperiksa terhadap instalasi 19.0 sebelum diwarisi. 

|**Model**|**Field pokok**|**Aturan dan hubungan**|
|---|---|---|
|tpr.material.family|name, grade, thickness_mm,<br>raw_product_id,<br>remnant_product_id,|Spesifikasi yang mengatur kesetaraan<br>produk dan kebijakan substitusi|
||scrap_product_id, company_id||



10 

|**Model**|**Field pokok**|**Aturan dan hubungan**|
|---|---|---|
|tpr.material.piece|name, family_id, lot_id, length_mm,<br>width_mm, shape,<br>measured_mass_kg, condition,<br>origin_mo_id, origin_project_id,<br>parent_piece_id, generated_at,<br>company_id|Identitas satu benda. Massa tersedia<br>diambil dari stok lot, bukan angka<br>saldo yang diedit|
|tpr.material.inspection|piece_id, decision, inspected_by,<br>inspected_at, criteria, note,<br>attachment_ids|Riwayat pemeriksaan dan<br>persetujuan, termasuk alasan turun<br>kelas|
|tpr.material.event|event_uid, event_type, effective_at,<br>company_id, family_id, piece_id,<br>source_ref, reversal_of_id|Header kejadian posted yang<br>menyimpan konteks dan bukti|
|tpr.material.event.line|event_id, role, mass_kg,<br>stock_move_line_id, mo_output_ref,<br>from_boundary, to_boundary,<br>measurement_method|Baris massa dengan kunci sumber<br>unik untuk klasifikasi dan neraca|
|tpr.production.balance|production_id, family_id,<br>baseline_version, planned_input_kg,<br>new_input_kg, reused_input_kg,<br>selected_output_kg, loss_kg,<br>wip_open_kg, wip_close_kg,<br>residual_kg, approval|Satu neraca per keluarga material<br>dan bagian MO yang selesai|
|tpr.material.reuse.request|source_piece_id, target_mo_id,<br>reserved_move_id,<br>requested_mass_kg, state,<br>approved_by|Reservasi tidak dianggap sebagai<br>konsumsi. Tidak boleh melampaui<br>massa tersedia|
|tpr.material.disposition|lot_ids, picking_id, sale_order_id,<br>direction, buyer_id,<br>weighed_mass_kg, price_basis,<br>amount, evidence,<br>recycling_evidence|Penyaluran mengacu ke delivery<br>done atau disposal yang sah|
|tpr.material.cash.record|disposition_id, date, amount,<br>currency_id, evidence, verified_by,<br>reversal_of_id|Opsional operasional, tidak<br>menggantikan jurnal akuntansi|



Tambahkan project_id pada MO dan relasi tombol pintar ke material piece, production balance, serta disposition. Piece memiliki origin_mo_id yang tetap sebagai asal penciptaan, sedangkan MO tujuan pemakaian ulang berada dalam riwayat event. Potongan yang dipotong ulang menghasilkan anak dan hubungan orang tua, tanpa menghilangkan hubungan proyek awal. 

Event posted bersifat append-only. Koreksi memakai reversal dan kejadian pengganti. Event generation dari produksi merujuk keluaran by-product. Event reuse merujuk konsumsi komponen remnant. Pengiriman 

11 

merujuk delivery. Stok awal historis merujuk inventory adjustment yang disahkan, dengan label bahwa asal proyek tidak diketahui bila bukti tidak ada. 

## **9 Aturan transaksi dan validasi** 

### **9.1 Validasi wajib** 

- Massa harus positif untuk transaksi fisik biasa. Reversal menggunakan dokumen koreksi yang jelas, bukan masukan massa negatif pada form biasa. 

- Lot, produk, family, company, grade, dan ketebalan harus konsisten. 

- Material yang belum diperiksa atau ditolak tidak dapat digunakan tanpa persetujuan teknis baru. 

- Pemakaian atau penyaluran tidak boleh melebihi saldo lot yang tersedia setelah reservasi. 

- Satu sumber move line hanya membentuk satu baris ledger untuk satu peran analitis. Gunakan unique constraint pada sumber dan peran yang relevan. 

- Memproses ulang MO, delivery, impor, atau request dengan event_uid sama harus menghasilkan transaksi lama atau penolakan, bukan stok tambahan. 

- MO yang tidak memiliki keluaran massa keluarga terpilih atau kehilangan yang belum dijelaskan tidak boleh disahkan sebagai neraca lengkap. 

- Selisih di luar toleransi memerlukan koreksi data atau pengecualian supervisor dengan alasan. Selisih tetap ditampilkan setelah pengecualian. 

- Tanggal efektif dan tanggal input harus tersimpan. Periode yang sudah dikunci tidak dapat diubah oleh operator. 

- Transaksi antarcompany tidak boleh dibuat melalui perubahan company_id yang melewati record rule. 

### **9.2 Penyelesaian MO dan by-product** 

Addon mengikuti workflow resmi MO. Tombol selesai dapat memunculkan wizard backorder atau langkah tambahan. Event hanya dibuat setelah move yang relevan benar-benar done. Jangan membuat event ketika action baru mengembalikan wizard. Jika MO selesai sebagian, sumber kejadian dan baseline dialokasikan menurut bagian yang selesai dan diuji bersama backorder. 

By-product dipakai untuk remnant dan scrap yang masih tersimpan fisik. Setelah dibuat dari MO, transfer ke lokasi karantina atau lokasi scrap dilakukan dengan dokumen stok standar. Jangan menambah inventory adjustment untuk sisa yang sudah ada pada by-product, karena tindakan itu menggandakan stok. 

### **9.3 Pemotongan ulang dan pembatalan** 

MVP menggunakan aturan bahwa satu operasi pemotongan mengonsumsi benda induk secara penuh. Keluaran terdiri atas komponen jadi, satu atau beberapa benda anak, scrap, serta kehilangan. Jika suatu pekerjaan hanya mereservasi material lalu dibatalkan, reservasi dilepas dan tidak ada keluaran baru. Jika bahan sudah dipotong, riwayatnya tidak dibatalkan seolah benda induk masih utuh. 

Pembatalan dokumen yang sudah memindahkan stok mengikuti retur atau koreksi resmi Odoo. Ledger harus mempunyai reversal yang sesuai. Larang penghapusan catatan posted. Koreksi ukuran atau hasil inspeksi dicatat sebagai revisi metadata dengan pengguna, waktu, dan alasan. 

12 

### **9.4 Kebijakan biaya** 

MVP menguji kuantitas, penelusuran, dan informasi penjualan. Kebijakan biaya by-product harus dinyatakan sebelum laporan nilai aset digunakan. Cost share by-product nol dapat dipakai sebagai kebijakan prototipe, dengan konsekuensi nilai stok akuntansinya tidak merepresentasikan potensi nilai guna potongan. Pembagian biaya yang berbeda memerlukan persetujuan perusahaan dan pengujian valuation. 

Potensi nilai jual adalah massa yang berpotensi dijual dikali harga penawaran per kg pada tanggal tertentu. Nilai tersebut merupakan estimasi. Pendapatan penjualan, penerimaan uang, nilai persediaan, dan laba harus memiliki field serta label yang berbeda. 

## **10 MFA dan rumus indikator** 

### **10.1 Batas sistem** 

Gunakan tiga batas analisis yang diberi label eksplisit. Pertama, batas proses atau MO untuk menguji pembentukan produk dan sisa. Kedua, batas gudang sisa untuk memeriksa stok remnant dan scrap fisik. Ketiga, batas perusahaan untuk memeriksa aliran eksternal. Ketiganya menggunakan periode dan keluarga material yang sama ketika dibandingkan. 

Transfer remnant antarlokasi dan konsumsi ulang internal bukan masukan eksternal perusahaan. Pada batas gudang sisa, perpindahan ke produksi menjadi keluaran gudang. Pada batas proses, remnant yang dikonsumsi menjadi masukan MO tujuan. Perbedaan ini mencegah massa yang sama dijumlah berulang sebagai bahan baru. Prinsip pembatasan proses dan konservasi massa merupakan dasar MFA, sedangkan rumus operasional berikut adalah rancangan indikator penelitian (Hagedorn et al., 2024). 

### **10.2 Neraca produksi** 

Untuk setiap MO dan keluarga material, total massa masukan baru dan ulang ditambah WIP awal harus sama dengan massa yang masuk ke produk, remnant, scrap fisik, kehilangan proses, dan WIP akhir, ditambah residual. WIP merupakan massa material terpilih yang masih berada dalam proses, bukan nilai biaya pekerjaan. 

I_baru + I_ulang + WIP_awal = P + R + S + L + WIP_akhir + e 

P adalah massa keluarga material yang menjadi produk atau komponen. R adalah remnant yang dikembalikan sebagai stok. S adalah scrap fisik yang ditimbang dan disimpan. L adalah kehilangan proses yang terukur atau diestimasi dengan metode yang dicatat. e adalah residual atau selisih belum terjelaskan. Sistem dilarang mengisi L secara otomatis dengan residual hanya agar neraca terlihat seimbang. 

Untuk MO yang selesai dan tidak memiliki WIP, massa proses D = I_baru + I_ulang. Yield = P / D x 100 persen. Proporsi remnant = R / D x 100 persen. Proporsi scrap = S / D x 100 persen. Proporsi kehilangan = L / D x 100 persen. Proporsi input ulang = I_ulang / D x 100 persen. Kelima persentase ini tidak dijumlah sebagai satu komposisi karena proporsi input ulang berada di sisi masukan. 

deviasi_rencana_pct = (D - rencana_input_kg) / rencana_input_kg x 100 

Deviasi positif menunjukkan konsumsi di atas baseline, sedangkan nilai negatif menunjukkan konsumsi di bawah baseline. Perbandingan hanya sah untuk spesifikasi, jumlah output, revisi desain, dan lingkup bahan yang sebanding. Baseline harus direvisi secara terkendali jika pekerjaan berubah. 

13 

### **10.3 Neraca gudang sisa** 

stok_awal + sisa_masuk + retur_ke_gudang 

= konsumsi_ulang + penjualan_done + disposal_done + stok_akhir + e 

Reklasifikasi dari reusable menjadi scrap tidak menjadi aliran keluar pada gabungan gudang sisa. Bila reusable dan scrap dilaporkan terpisah, reklasifikasi antarjenis tampil sebagai perpindahan internal yang mengurangi satu kategori dan menambah kategori lain dengan massa yang sama. 

Persentase pemakaian ulang gudang periode = konsumsi ulang selama periode dibagi stok awal reusable ditambah remnant baru yang diterima dan retur valid selama periode, dikali 100 persen. Tampilkan numerator dan denominator. Untuk evaluasi lebih kuat, laporan kohort dapat mengikuti potongan yang lahir pada periode tertentu dan melaporkan bagian yang sudah dimanfaatkan sampai tanggal evaluasi. 

### **10.4 Umur stok dan kualitas data** 

Umur dihitung dari tanggal fisik potongan terbentuk, bukan tanggal terbaru transfer. Anak hasil pemotongan mempunyai tanggal pembentukan sendiri dan tetap membawa asal garis keturunan. Stok historis yang tidak diketahui tanggalnya mendapat status umur tidak diketahui. 

Saldo per tanggal historis dihitung dari seluruh move done sampai batas waktu, termasuk opening, retur, dan koreksi. Menggunakan stock.quant saat ini lalu mengganti filter tanggal tidak menghasilkan stok historis. Tentukan waktu perusahaan Asia/Jakarta untuk penyajian dan simpan datetime menurut mekanisme UTC Odoo. Tanggal akhir laporan dipakai sebagai batas awal hari berikutnya agar transaksi pukul 23.59 tidak terlewat. 

Ketika denominator nol, dashboard menampilkan N A dan alasan. KPI hanya mencakup transaksi posted dengan sumber sah. Tampilkan proporsi massa estimasi, jumlah catatan tanpa bukti, dan residual sebagai indikator kualitas data. Nilai agregat yield dihitung dari total P dibagi total D, bukan rerata sederhana persentase antarMO. 

## **11 Dashboard dan kebutuhan tampilan** 

### **11.1 Dashboard Firdaus** 

|**Indikator**|**Definisi**|**Tindak lanjut pengguna**|
|---|---|---|
|Stok remnant<br>tersedia|Kg per grade dan ketebalan, jumlah<br>benda dan lokasi|Cari kandidat untuk proyek berikutnya|
|Stok scrap fisik|Kg yang masih berada di lokasi internal<br>siap salur|Rencanakan pemeriksaan dan penjualan|
|Umur stok|Hari sejak pembentukan, kelompok umur<br>yang dapat diatur|Tinjau potongan yang lama belum<br>ditindaklanjuti|
|Pemakaian ulang<br>aktual|Kg remnant yang benar-benar dikonsumsi<br>MO selama periode|Telusuri asal potongan dan proyek tujuan|



14 

|**Indikator**|**Definisi**|**Tindak lanjut pengguna**|
|---|---|---|
|Penyaluran aktual|Kg delivery atau disposal done selama<br>periode|Cocokkan dengan bukti timbang dan<br>penerima|
|Nilai penjualan dan<br>penerimaan uang|Nilai transaksi sah dan catatan uang<br>terverifikasi, ditampilkan terpisah|Rekonsiliasi dengan dokumen perusahaan|
|Neraca gudang sisa|Stok awal, masuk, keluar, akhir, dan<br>residual|Periksa selisih serta data belum lengkap|



### **11.2 Dashboard Feriangga** 

|**Indikator**|**Definisi**|**Tindak lanjut pengguna**|
|---|---|---|
|Status MO proyek|Rencana, berjalan, selesai sebagian,<br>selesai|Pantau pekerjaan dan kelengkapan catatan|
|Input baru dan<br>ulang|Kg bahan yang benar-benar dikonsumsi|Periksa penggunaan stok baru dan remnant|
|Yield material|Total massa pelat pada produk dibagi<br>total input proses|Bandingkan pekerjaan yang sebanding|
|Deviasi bahan|Perbedaan aktual terhadap baseline yang<br>disetujui|Telusuri perubahan kebutuhan dan konsumsi|
|Komposisi<br>keluaran|Produk, remnant, scrap, kehilangan,<br>residual|Tentukan bagian proses yang perlu diperiksa|
|Kualitas<br>pencatatan|Massa estimasi, neraca belum lengkap,<br>dan pengecualian|Prioritaskan verifikasi data produksi|



### **11.3 Interaksi dan konsistensi angka** 

Filter meliputi company, periode, proyek, family, grade, ketebalan, lokasi, dan metode pengukuran. Kartu KPI dapat diklik untuk membuka transaksi pembentuknya. Grafik keluaran produksi tidak mencampur stock snapshot dengan aliran periode. Tampilkan waktu refresh serta keterangan apakah data aktual atau estimasi. 

Graph dan pivot menjadi verifikasi pertama. Dashboard OWL memakai service ORM dan kontrol akses yang sama. Refresh manual wajib tersedia. Pembaruan setiap 60 detik boleh ditambahkan untuk demo dengan label waktu pembaruan. Istilah real time tidak digunakan untuk menjanjikan informasi yang belum diinput operator. 

Ekspor CSV memuat filter, waktu pengambilan, sumber transaksi, satuan, dan numerator serta denominator KPI. Hasil yang dilihat pengguna harus sama dengan data yang diunduhnya. Operator tidak dapat membuka pendapatan atau catatan uang jika aksesnya dibatasi. 

15 

## **12 Peran pengguna dan pengendalian akses** 

|**Peran**|**Hak pokok**|**Batasan**|
|---|---|---|
|Administrator<br>sistem|Instalasi, konfigurasi, pengguna, dan<br>pemeliharaan|Tidak menjadi alasan melewati persetujuan<br>bisnis|
|Planner produksi|Proyek, BoM, baseline, MO, usulan<br>substitusi|Tidak mengesahkan kelayakan teknis sendiri<br>jika perusahaan memisah peran|
|Operator produksi|Input aktual, massa keluaran, foto, dan<br>usulan sisa|Tidak menghapus posted atau mengubah<br>periode terkunci|
|Petugas gudang|Penerimaan, lokasi, identitas, transfer,<br>dan pemeriksaan stok|Tidak melihat catatan keuangan bila tidak<br>diperlukan|
|Supervisor|Pemeriksaan teknis, approval neraca,<br>pengecualian, koreksi|Alasan dan bukti tetap wajib|
|Pemilik atau<br>manajemen|Dashboard dan persetujuan penyaluran|Akses sesuai company dan kebijakan<br>perusahaan|
|Peneliti|Data uji dan laporan sesuai izin|Data perusahaan hanya dalam lingkup<br>penelitian yang disepakati|



ACL, record rule company, keamanan field sensitif, dan akses tombol harus konsisten. Sembunyinya tombol tidak cukup untuk mencegah pemanggilan method dari RPC. Pembatasan harus ditegakkan pada server. Dashboard tidak menggunakan sudo untuk memberi angka lintascompany atau field keuangan kepada pengguna yang tidak berwenang. 

## **13 Lingkungan pengembangan dan struktur repository** 

### **13.1 Susunan project Antigravity** 

Repository berisi addons dengan empat addon utama, folder config untuk odoo.conf, compose.yaml, .env.example, folder docs, folder tests, serta folder demo. Pisahkan addon pihak ketiga pada third_party_addons. Simpan README berisi instalasi, upgrade, test, dan pemulihan. Keputusan penting dicatat pada docs/decisions.md. 

Setiap addon memiliki __manifest__.py, __init__.py, models, security, views, data, dan tests. Wizard diletakkan pada folder wizard. Dashboard OWL memakai static/src dan asset bundle yang sesuai Odoo 19. Nama XML ID memakai awalan addon sendiri dan tidak mengganti file core. 

### **13.2 Docker dan konfigurasi awal** 

Minta agen menyiapkan Compose menggunakan image resmi odoo:19.0 dan PostgreSQL 16, lalu memverifikasi tag dan kompatibilitas dari sumber resmi ketika dijalankan. Pin digest yang benar-benar berhasil dipakai pada hasil final. Konfigurasi addon path mencakup addon bawaan, addon khusus, dan addon pihak ketiga yang disetujui. Database serta filestore menggunakan volume persisten. 

16 

Bind port web ke 127.0.0.1:8069 untuk demonstrasi lokal. Jangan expose port database ke internet. Gunakan secret lokal untuk password database dan master password, simpan .env dalam gitignore, dan berikan .env.example tanpa secret aktual. Nama database terpisah untuk pengembangan dan pengujian, misalnya tpr_ce_dev dan tpr_ce_test. 

### **13.3 Perintah yang wajib disediakan agen** 

docker compose up -d db odoo 

docker compose exec odoo odoo --version 

docker compose logs --tail=100 odoo 

Perintah di atas merupakan kontrak nama service yang harus diwujudkan oleh Compose. Untuk instalasi atau upgrade addon, agen harus menyediakan perintah lengkap dengan config, host database, kredensial melalui environment atau konfigurasi, addons path, nama database, daftar addon, dan --stop-after-init yang cocok dengan hasil instalasinya. 

Jalankan instalasi dan test melalui service one-off tersendiri ketika web server yang sama sudah berjalan, agar tidak berebut port atau proses upgrade database. Test menggunakan database terpisah. Perintah uninstall, penghapusan volume, dan reset data tidak boleh menjadi langkah otomatis tanpa kebutuhan yang jelas. 

### **13.4 Pemulihan** 

Backup harus mencakup database PostgreSQL, filestore Odoo, kode addon, versi image, dan konfigurasi yang dapat dipulihkan tanpa menaruh secret ke repository. Lakukan satu restore ke database uji dan periksa identitas potongan serta lampiran bukti. Screenshot tanpa backup data tidak cukup sebagai arsip penelitian. 

## **14 Urutan pembangunan dan kriteria selesai** 

|**Tahap**|**Pekerjaan**|**Kriteria selesai**|
|---|---|---|
|0 Pemeriksaan<br>lingkungan|Odoo 19, edisi, Docker, source core, dan<br>addon|Versi dan dependensi dicatat, database uji<br>tersedia|
|1 Fondasi standar|Company, produk, lokasi, proyek,<br>pembelian, dan MO|Satu alur receipt sampai MO dan delivery<br>berjalan|
|2 Core material|Family, piece, measurement, inspeksi,<br>ledger, dan ACL|Identitas serta pembatasan akses dapat diuji|
|3 Manufacturing<br>CE|Baseline, konsumsi, keluaran massa, dan<br>validasi|MO uji menghasilkan neraca dan by-product<br>satu kali|
|4 Waste<br>Management|Karantina, pencarian, reservasi, anak<br>potongan, penyaluran|Satu potongan dapat dilacak sampai MO<br>berikutnya dan penjualan|
|5 Laporan dasar|Graph, pivot, snapshot, dan rumus|Semua angka cocok dengan data acuan<br>manual|



17 

|**Tahap**|**Pekerjaan**|**Kriteria selesai**|
|---|---|---|
|6 Dashboard dan<br>ekspor|Kartu KPI, filter, drilldown, dan CSV|Angka tampilan serta ekspor sama untuk<br>pengguna yang sama|
|7 Evaluasi<br>lapangan|Data nyata terbatas, uji pengguna, dan<br>koreksi|Skenario dan temuan disahkan pihak yang<br>berwenang|
|8 Dokumentasi|Panduan, log test, versi, backup dan<br>restore|Demo dapat diulang dari lingkungan bersih|



Quickstart dioperasionalkan menjadi kick-off call, analysis, dan configuration. Kick-off menetapkan masalah, pengguna, tujuan, serta batas penelitian. Analysis menghasilkan proses existing, proses usulan, fit gap, kebutuhan data, dan indikator. Configuration mencakup konfigurasi, addon, migrasi terbatas, pelatihan, dan pengujian. Tahap teknis pada tabel merupakan rincian pekerjaan di dalam kerangka itu, bukan penamaan metodologi baru (Lutfiah et al., 2024). 

Validasi kebutuhan dilakukan sebelum pengembangan rinci. Keinginan membangun sistem lebih dahulu dapat dilaksanakan setelah baseline masalah dan proses disepakati. Catat setiap revisi agar laporan penelitian menjelaskan keputusan nyata yang terjadi. 

## **15 Data demonstrasi dan perhitungan acuan** 

Semua angka pada bagian ini merupakan data simulasi untuk menguji sistem. Angka tersebut bukan hasil pengukuran CV Teknika Prima Raya. 

### **15.1 Proyek pertama** 

MO A memproses 100 kg pelat MS 3 mm dari bahan baru. Massa pelat pada komponen jadi adalah 72 kg. Remnant terdiri atas benda R1 sebesar 8 kg dan R2 sebesar 12 kg. Scrap fisik 6 kg disimpan, dan kehilangan pemotongan terukur 2 kg dicatat dengan metode serta bukti uji. 

100 = 72 + 8 + 12 + 6 + 2 

Yield MO A sebesar 72 persen. Remnant 20 persen, scrap fisik 6 persen, dan kehilangan 2 persen. Residual nol. Saldo gudang sisa sesudah MO A adalah 26 kg, terdiri atas reusable 20 kg dan scrap fisik 6 kg. 

### **15.2 Proyek kedua memakai R1** 

MO B memakai R1 seluruhnya sebanyak 8 kg. Keluaran berupa komponen 5,5 kg, remnant anak R1A sebesar 2 kg, dan scrap 0,5 kg. Tidak ada kehilangan proses pada data simulasi ini. R1 habis secara stok, R1A mempunyai lot baru, dan origin project pertama tetap dapat ditelusuri melalui hubungan induk. 

8 = 5.5 + 2 + 0.5 

Yield MO B sebesar 68,75 persen dan proporsi input ulang 100 persen. Pemakaian ulang yang dicatat adalah 8 kg bahan yang benar-benar dikonsumsi, sedangkan massa yang menjadi komponen dari proses itu adalah 5,5 kg. Kedua angka mempunyai pengertian berbeda. 

18 

### **15.3 Penjualan dan neraca periode** 

Sebanyak 4 kg dari batch scrap pertama dijual dan delivery disahkan. Sebelum delivery done, stok tidak berkurang. Jika harga simulasi Rp5.000 per kg, nilai transaksi 4 kg adalah Rp20.000. Jika pembeli baru membayar Rp10.000, catatan uang diterima adalah Rp10.000 dan harus ditampilkan terpisah dari nilai transaksi. 

Stok remnant akhir adalah R2 12 kg ditambah R1A 2 kg, yaitu 14 kg. Scrap akhir adalah 6 kg ditambah 0,5 kg dikurangi 4 kg, yaitu 2,5 kg. Total gudang sisa akhir adalah 16,5 kg. 

gudang_sisa 0 + 26 + 2.5 = 8 + 4 + 16.5 

Massa sisa baru pada batas gudang meliputi 26 kg dari MO A dan 2,5 kg dari MO B. Konsumsi ulang 8 kg menjadi keluaran gudang. Pada batas perusahaan, sirkulasi internal 8 kg tidak dijumlah sebagai masukan baru. 

perusahaan 100 = produk 77.5 + penjualan 4 + kehilangan 2 + stok_sisa_akhir 16.5 Agregat yield per operasi adalah 77,5 dibagi 108 kg input proses, yaitu sekitar 71,76 persen. Angka tersebut berbeda dari rasio produk terhadap masukan eksternal perusahaan, yaitu 77,5 dibagi 100 atau 77,5 persen. Label dan batas kedua indikator harus ditampilkan agar pembaca tidak menyamakan keduanya. 

## **16 Pengujian dan kriteria penerimaan** 

### **16.1 Skenario minimum** 

|**Kode**|**Skenario**|**Hasil yang harus terjadi**|
|---|---|---|
|T01|Receipt 100 kg bahan baru|Saldo lot 100 kg, family dan company benar|
|T02|MO A selesai|Produk 72, remnant 20, scrap 6, kehilangan 2 dan residual<br>0|
|T03|MO A diproses ulang|Tidak ada lot, stok, atau ledger ganda|
|T04|Reservasi R1 ke MO B|Available turun sesuai reservasi, KPI reuse tetap 0<br>sebelum konsumsi|
|T05|Pemakaian R1 ke MO B|R1 habis, R1A 2 kg, scrap tambahan 0,5 kg, traceability<br>lengkap|
|T06|Pemakaian lebih dari saldo|Penolakan server tanpa transaksi parsial|
|T07|Lot salah grade atau belum layak|Penolakan dan alasan yang dapat dipahami|
|T08|Delivery scrap draft lalu done|Stok berkurang hanya setelah done|
|T09|Penjualan parsial dan retur|Hanya kuantitas done dihitung, retur memulihkan saldo<br>dan mengoreksi aliran|
|T10|Neraca tidak seimbang|Tidak otomatis menjadi kehilangan, supervisor dapat<br>melihat residual|



19 

|**Kode**|**Skenario**|**Hasil yang harus terjadi**|
|---|---|---|
|T11|Selesai sebagian dan backorder MO|Bagian selesai tercatat sekali, sisa rencana dialokasikan<br>dengan benar|
|T12|Operator membuka data uang|Akses server ditolak sesuai ACL dan field security|
|T13|Dua pengguna memesan R1 bersamaan|Hanya satu reservasi valid, tidak ada stok negatif atau<br>pemakaian ganda|
|T14|Filter historis dan waktu Jakarta|Stok awal akhir mengikuti move pada tanggal yang benar|
|T15|Denominator nol dan massa estimasi|N A serta penanda estimasi tampil dengan benar|
|T16|Ekspor dan drilldown|Jumlah sama dengan KPI dan sesuai akses pengguna|
|T17|Reklasifikasi remnant menjadi scrap|Total massa tetap, produk lama turun dan produk baru<br>naik sekali|
|T18|Restore backup|Database, lot, relasi, dan lampiran kembali dapat dibuka|



### **16.2 Ketelitian dan performa** 

Toleransi perhitungan perangkat lunak pada data acuan ditetapkan berdasarkan rounding satuan yang dikonfigurasi. Perbandingan fisik memakai ketidakpastian alat yang disepakati, bukan toleransi software. Selisih massa fisik perlu diperiksa pada grade dan periode yang sama. 

Target awal dashboard adalah respons paling lama tiga detik untuk 5.000 baris kejadian pada mesin demo, dengan ukuran, hardware, dan jumlah pengguna dicatat. Target ini merupakan kriteria proyek yang diuji, bukan klaim performa bawaan Odoo. Optimasi dan indeks ditambahkan setelah pengukuran menunjukkan kebutuhan. 

UAT melibatkan peran yang benar-benar menangani bahan, produksi, dan keputusan penyaluran. Catat tugas, keberhasilan, waktu, kesalahan, komentar, dan revisi. Jumlah partisipan serta alasan pemilihannya dilaporkan apa adanya. UAT yang berhasil tidak otomatis membuktikan penurunan waste atau peningkatan keuntungan. 

### **16.3 Definition of done** 

Sistem dinyatakan siap demo apabila instalasi bersih, upgrade addon, pengujian angka, kontrol akses, skenario integrasi, ekspor, dan restore berhasil. Setiap hasil test memiliki tanggal, commit, kondisi data, expected result, actual result, dan status. Daftar bug yang belum diselesaikan disertai dampak terhadap penggunaan serta indikator yang terpengaruh. 

20 

## **17 Prompt lengkap untuk Antigravity** 

Salin seluruh teks mulai bagian 17.1 sampai akhir bagian 17.12 sebagai satu instruksi agen. Bagian 18 dapat digunakan setelah agen menyelesaikan fondasi. Nama model khusus di dalam prompt merupakan rancangan proyek. Agen wajib memeriksa API asli instalasi Odoo 19 sebelum menulis extension. 

### **17.1 Peran agen dan tujuan pekerjaan** 

Kamu bertindak sebagai pengembang senior Odoo 19 Community dan penguji integrasi. Bangun sistem yang benar-benar dapat dipasang serta dijalankan untuk prototipe dua Tugas Akhir di CV Teknika Prima Raya. Gunakan Antigravity sebagai IDE. Hasil kerja adalah repository yang berisi addon Odoo, konfigurasi pengembangan, data demo yang jelas berlabel simulasi, pengujian, dan dokumentasi. Lanjutkan pekerjaan sampai alur integrasi dan kriteria penerimaan tercapai. Jangan berhenti pada rencana, mockup, file kosong, atau dashboard dengan angka statis. 

Sistem memakai satu database. Feriangga mengembangkan Manufacturing dan analisis efisiensi penggunaan pelat. Firdaus mengembangkan Waste Management dengan MFA untuk sisa pelat. Keduanya mengadopsi Circular Economy melalui pemeriksaan sisa, pemakaian ulang internal, dan penyaluran scrap yang tercatat. Jangan membuat klaim penurunan emisi, peningkatan laba, atau penyelesaian modal kerja dari data simulasi. 

### **17.2 Pemeriksaan wajib sebelum implementasi** 

Periksa repository dan AGENTS.md yang tersedia. Identifikasi apakah project sudah memiliki instalasi Odoo, Compose, konfigurasi, database, addon, atau data perusahaan. Pertahankan pekerjaan yang telah ada. Tentukan versi menggunakan executable Odoo dan source code, serta pastikan edisinya Community dan major version 19.0. Jika lingkungan ternyata berbeda, laporkan konflik spesifik dan jangan menulis kode yang mengaku kompatibel tanpa pemeriksaan. 

Baca manifest dan source model 19.0 untuk mrp.production, mrp.bom, stock.move, stock.move.line, stock.lot, stock.picking, stock.scrap, product.product, serta satuan. Pastikan field kuantitas, API reservasi dan completion, workflow backorder, format constraint, sintaks view, asset bundle, dan service OWL sesuai 19.0. Jangan menyalin implementasi 16 atau 17 secara langsung. Buat docs/version_audit.md berisi versi, edisi, modul tersedia, keputusan kompatibilitas, dan referensi source yang diperiksa. 

Periksa addon pihak ketiga hanya dari source yang dapat dilihat manifest dan lisensinya. Syarat proyek adalah tanpa dependensi berbayar. Jangan bergantung pada Studio, spreadsheet dashboard berlisensi khusus, atau modul Enterprise. OCA web_responsive dan stock_no_negative boleh dipertimbangkan setelah verifikasi cabang 19.0 dan test, namun sistem inti wajib tetap dapat berjalan tanpa keduanya. 

### **17.3 Struktur hasil yang harus dibuat** 

Buat compose.yaml, config/odoo.conf, .env.example, .gitignore, README.md, folder addons, third_party_addons, docs, tests, dan demo. Addon utama adalah tpr_circular_core, tpr_manufacturing_ce, tpr_waste_management, dan tpr_circular_dashboard. Gunakan lisensi addon khusus yang kompatibel dengan distribusi dan dependensi aktual, lalu dokumentasikan pilihannya. Jangan mengubah source core Odoo. 

21 

Core bergantung pada modul standar yang dibutuhkan, termasuk stock, mrp, project, mail, dan web. Manufacturing CE serta Waste Management bergantung pada core dengan tambahan standar masingmasing. Dashboard bergantung pada core dan dua addon penelitian. Hindari circular dependency. Jika integrasi pembayaran memakai account, tempatkan pada addon opsional terpisah. 

Gunakan image resmi Odoo 19.0 dan PostgreSQL 16 untuk lingkungan demo, lalu verifikasi keduanya sebelum pin versi atau digest. Siapkan volume database dan filestore, addon path yang benar, healthcheck, serta database pengujian terpisah. Port demo hanya bind ke localhost. Jangan menulis password aktual di kode, log, atau README. 

### **17.4 Spesifikasi master data** 

Bangun tpr.material.family untuk grade, ketebalan, raw_product_id, remnant_product_id, scrap_product_id, company_id, dan parameter pemeriksaan. Gunakan kg untuk stok pelat, remnant, dan scrap. Simpan dimensi mm secara terpisah. Produk hasil boleh unit, tetapi massa keluarga material pada keluaran harus dicatat tersendiri. 

Produk demo minimal PLT_MS_3, REM_MS_3, SCR_MS_3, dan dua produk komponen hasil. Lokasi internal minimal Bahan Baru, Karantina Sisa, Sisa Layak, dan Scrap Siap Salur. Scrap siap dijual tetap berada di lokasi internal. Virtual scrap digunakan hanya untuk barang yang benar-benar dikeluarkan dari inventaris sebagai pembuangan. 

Satu benda remnant menggunakan satu stock.lot dan satu tpr.material.piece. Lot menyimpan kg benda tersebut, bukan satu unit serial. Piece memiliki identitas, family, lot, panjang, lebar, bentuk, kondisi, massa saat pembentukan, cara ukur, asal MO, asal proyek, parent_piece_id, generated_at, bukti, dan company. Saldo tersedia piece berasal dari lot di stok standar. Jangan menyimpan saldo bebas yang dapat diedit pengguna. 

Master company demo bernama CV Teknika Prima Raya. Jangan mengisi nomor pajak, rekening, kontak personal, omzet, atau kapasitas produksi yang tidak diberikan. Data operasional contoh wajib mempunyai penanda demo agar tidak tertukar dengan data penelitian nyata. 

### **17.5 Spesifikasi Manufacturing CE** 

Tambahkan project_id pada MO dan tombol pintar ke neraca, sisa, dan riwayat material. Simpan baseline kebutuhan bahan dengan versi, tanggal, dan alasan perubahan. Gunakan BoM serta workflow MO standar untuk rencana dan actual consumption. Penerbitan bahan atau reservasi tidak dianggap konsumsi sebelum posting yang sesuai. 

Bangun tpr.production.balance per MO, bagian completion, dan family. Simpan massa input baru, input ulang, massa keluarga material pada produk, remnant, scrap fisik, kehilangan, WIP awal akhir, serta residual. Keluaran massa produk harus berasal dari pengukuran atau estimasi yang dijelaskan. Jangan mengambil berat seluruh assembly bila hanya pelat tertentu yang menjadi batas analisis. 

Gunakan by-product standar untuk remnant dan scrap yang masih disimpan. Jumlah by-product harus aktual. Pada completion final atau partial, buat piece dan event hanya untuk move done yang benar-benar terjadi. Wizard backorder yang baru muncul belum menjadi dasar event. Cegah posting berulang dari button_mark_done atau metode lain. Periksa nama hook asli 19.0 sebelum membuat override. 

22 

Validasi persamaan I_baru + I_ulang + WIP_awal = P + R + S + L + WIP_akhir + residual. Jangan mengisi kehilangan sebagai angka otomatis untuk menutup residual. Jika residual melebihi toleransi, minta koreksi data atau pengecualian supervisor dengan alasan dan tetap tampilkan residual. Jangan menghilangkan hasil pengukuran awal saat pengecualian diberikan. 

### **17.6 Spesifikasi Waste Management** 

Buat list, form, search, graph, dan pivot untuk piece, inspection, reuse request, disposition, dan event. Sediakan filter grade, ketebalan, dimensi, kondisi, lokasi, umur, proyek asal, serta status pemeriksaan. Buat tombol untuk membuka lot dan semua transaksi terkait. 

Catatan baru dari produksi masuk karantina. Supervisor teknis mencatat hasil pemeriksaan reusable, scrap untuk penyaluran, atau perlu pemeriksaan. Pindahkan stok dengan picking standar yang sesuai. Reklasifikasi produk remnant menjadi scrap harus memakai input dan output konversi yang sama massa, bukan mengubah label lalu menambah quant baru. Dokumentasikan metode konversi yang dipilih dan uji akibatnya terhadap quantity serta valuation. 

Pencarian kandidat memfilter kesetaraan family, ketebalan, grade, ukuran minimal, kondisi, dan saldo tersedia. Untuk persegi panjang, boleh mempertimbangkan rotasi 90 derajat. Potongan tidak beraturan wajib ditandai perlu pemeriksaan manual. Urutan dapat memprioritaskan umur paling lama lalu ukuran yang lebih mendekati kebutuhan. Urutan tersebut adalah heuristik eksplisit, bukan optimasi nesting. 

Wizard reuse menghubungkan source piece dengan target MO, memeriksa kompatibilitas, menyimpan approval, dan menyiapkan reservasi standar. Substitusi produk bahan baru dengan remnant harus mempertahankan baseline dan meniadakan konsumsi ganda. Jangan membuat kuantitas komponen remnant langsung melalui perubahan stock.quant. 

Untuk operasi pemotongan, konsumsi benda induk seluruhnya. Bentuk potongan anak dengan lot baru apabila masih ada sisa. Anak membawa parent_piece_id dan asal proyek yang dapat ditelusuri. Pembatalan reservasi belum dipotong mengembalikan availability tanpa menghasilkan potongan baru. Jika sudah dipotong, lakukan koreksi sesuai keadaan fisik dan jangan menghidupkan kembali induk utuh. 

Penyaluran scrap menggunakan sale order dan delivery atau disposal yang sah. Simpan pembeli, hasil timbang, harga per kg dan tanggalnya, bukti, lot batch, serta hubungan dokumen. Stock berkurang hanya ketika move done. Recycle completed hanya boleh digunakan bila recycling_evidence tersedia. Penjualan tanpa bukti pengolahan tampil sebagai sold atau dispatched. 

Jika account belum dipakai, buat cash record operasional yang menyimpan amount, currency, tanggal, bukti, verifikator, dan reversal. Label jelas bahwa ini bukan ledger akuntansi. Pisahkan nilai transaksi, uang diterima, estimasi potensi jual, dan book value. 

### **17.7 Ledger dan integritas data** 

Buat tpr.material.event dan event.line untuk generation, reuse consumption, dispatch, disposal, opening, return, reclassification, loss observation, dan correction. Setiap event punya event_uid, waktu efektif, waktu input, company, sumber, dan reversal_of_id. Setiap line mempunyai family, role, massa, sumber move line atau output record, serta batas proses asal tujuan. 

23 

Stok standar adalah sumber kebenaran quantity. Ledger berfungsi untuk klasifikasi dan neraca. Hindari salinan quantity yang dapat diedit. Posting memakai transaksi atomik Odoo. Unique constraint harus mencegah sumber dan peran yang sama dicatat dua kali. Event posted tidak boleh dihapus atau diedit bebas. Koreksi membentuk reversal dan pengganti yang saling terkait. 

Pengguna tidak boleh meminta reuse melebihi available setelah reservasi. Tangani concurrency melalui reservasi dan penguncian sesuai ORM yang benar, bukan hanya pengecekan di browser. Dua request bersamaan untuk benda yang sama tidak boleh keduanya berhasil. Buat test konkurensi atau pembuktian transaksi yang memperlihatkan pencegahannya. 

Simpan company_id pada model yang membutuhkan dan terapkan check_company serta record rule yang sesuai. Periksa input method server, bukan hanya attrs atau visibility tombol. Hindari sudo pada angka dashboard dan field sensitif. Parameter impor, filter, dan query harus divalidasi. 

### **17.8 Rumus dan laporan** 

Gunakan tiga batas berlabel: MO, gudang sisa, dan perusahaan. Transfer internal tidak menjadi masukan eksternal. Pada gudang sisa, reuse consumption menjadi aliran keluar ke produksi. Generation remnant dari MO berikutnya menjadi aliran masuk baru ke gudang. Pada batas perusahaan, kedua aliran internal itu tidak menambah total bahan dari luar. 

Untuk MO selesai tanpa WIP: D = input baru + input ulang. Yield = P / D x 100. Remnant fraction = R / D x 100. Scrap fraction = S / D x 100. Loss fraction = L / D x 100. Reused input fraction = input ulang / D x 100. Deviasi baseline = (D - planned_input_kg) / planned_input_kg x 100. Proporsi input ulang ditampilkan terpisah dari komposisi keluaran. 

Neraca gudang sisa adalah opening + generation + return = reuse consumption + dispatch + disposal + closing + residual. Perpindahan reusable ke scrap pada gabungan gudang tidak menjadi penyaluran eksternal. Laporan per kategori tetap memperlihatkan reclassification masuk dan keluar. 

Massa snapshot historical dihitung dari move done dan koreksi sampai cutoff waktu. Jangan memakai quant saat ini untuk periode masa lalu. Gunakan Asia/Jakarta pada tampilan dan cutoff periode. Date akhir memakai batas eksklusif awal hari berikutnya. Simpan tanggal pembentukan piece untuk umur stok, dan jangan mereset umur pada transfer lokasi. 

Semua pembagian denominator nol menampilkan N A. Agregat yield memakai total P dibagi total D. Nilai estimasi ditandai dan proporsi massa estimasi ditampilkan. Klik KPI membuka daftar sumber. CSV harus menyertakan unit, periode, filter, numerator, denominator, dan sumber. 

### **17.9 Dashboard dan UX** 

Bangun dua menu dashboard terpisah. Dashboard Waste menampilkan stok remnant, stok scrap fisik, jumlah benda, umur, reuse aktual, dispatch aktual, nilai transaksi, catatan uang yang boleh diakses, serta neraca gudang. Dashboard Manufacturing menampilkan status MO, rencana dan actual material, yield, deviasi, proporsi input ulang, komposisi keluaran, serta completeness. 

Implementasikan laporan list graph pivot lebih dulu agar angka bisa diuji. Sesudah benar, buat kartu KPI OWL dan chart yang menggunakan service ORM serta asset Odoo 19. Setiap kartu punya unit dan waktu refresh. 

24 

Filter company, tanggal, proyek, family, grade, ketebalan, lokasi, dan metode ukur berlaku konsisten. Berikan empty state yang menjelaskan data belum tersedia. 

Tampilan operator memakai bahasa Indonesia dengan istilah bisnis yang mudah dipahami. Gunakan urutan form mengikuti aktivitas pengguna. Jangan menampilkan istilah internal seperti idempotency key kepada operator bila tidak dibutuhkan. Pesan error menyebut data yang harus diperbaiki. Jangan membuat UI cantik dengan nilai demo yang dihardcode pada perhitungan dashboard. 

### **17.10 Data acuan yang harus lulus** 

Buat data simulasi yang dapat diulang di database demo terpisah. MO A: input baru 100 kg, produk dengan massa pelat 72 kg, remnant R1 8 kg, R2 12 kg, scrap batch 6 kg, loss 2 kg. MO B: konsumsi R1 8 kg, produk 5,5 kg, anak R1A 2 kg, scrap 0,5 kg, loss 0. Dispatch 4 kg dari scrap pertama. Harga simulasi Rp5.000 per kg, nilai transaksi Rp20.000, pembayaran operasional simulasi Rp10.000. 

Expected closing remnant 14 kg, scrap fisik 2,5 kg, total gudang sisa 16,5 kg. Reuse actual 8 kg. Neraca perusahaan: input eksternal 100 = produk 77,5 + dispatch 4 + loss 2 + closing 16,5. Neraca gudang: 0 + 28,5 = reuse 8 + dispatch 4 + closing 16,5. Agregat yield proses 77,5 / 108 x 100 sekitar 71,76 persen, berbeda dari rasio produk terhadap input eksternal 77,5 persen. 

Gunakan record demo dan skrip seed idempotent. Jangan mengisi data demo otomatis ke database perusahaan. Berikan cara menyiapkan database demo bersih tanpa menghapus database yang sudah ada. 

### **17.11 Pengujian wajib dan bukti eksekusi** 

Buat test perhitungan dan test integrasi Odoo yang bermakna untuk receipt, MO final, partial completion, backorder, by-product, reuse, anak potongan, dispatch, retur, reklasifikasi, koreksi, dan repeated posting. Uji invalid mass, salah family, saldo tidak cukup, belum diperiksa, periode terkunci, akses lintascompany, dan akses catatan uang. Uji denominator nol dan filter historical cutoff. 

Jalankan test pada database terpisah menggunakan mekanisme test resmi Odoo 19. Catat perintah aktual, exit status, tanggal, versi, dan test yang dieksekusi. Jangan menulis semua test pass jika executable tidak tersedia atau perintah gagal. Jika lingkungan menghalangi eksekusi, laporkan blocker yang nyata, test yang belum dijalankan, dan perintah untuk mengulangnya. Tetap selesaikan pekerjaan lain yang bisa diverifikasi. 

Uji install bersih serta upgrade addon. Periksa dashboard melalui browser lokal atau pengujian UI yang tersedia setelah aplikasi dapat dibuka. Verifikasi klik KPI, filter, CSV, pesan error, empty state, dan hak pengguna. Ukur target tiga detik untuk 5.000 baris event pada hardware demo yang dicatat. Jangan menambah index atau query kompleks tanpa pengukuran. 

### **17.12 Dokumentasi dan penutupan pekerjaan** 

Hasil akhir wajib memuat source addon lengkap, manifest, security, views, wizard, data master, data simulasi, test, Compose, config, README, arsitektur, ERD, kamus data, daftar KPI dan rumus, panduan per peran, panduan backup restore, version audit, serta daftar keterbatasan yang masih ada. Siapkan docs/research_traceability.csv berisi masalah, requirement, fitur, test, hasil, dan pemilik penelitian. 

Berikan langkah run, install, upgrade, test, demo, dan restore dengan perintah yang cocok dengan struktur final. Pastikan demo dapat diulang dari lingkungan bersih. Berikan ringkasan file yang diubah, fitur yang 

25 

berhasil, test yang benar-benar dijalankan, dan pekerjaan tersisa. Semua keputusan asumsi proses perusahaan harus masuk docs/validation_questions.md untuk validasi pengguna, tanpa mengarang angka atau hasil wawancara. 

Kerjakan secara bertahap. Pada setiap tahap, lakukan implementasi, verifikasi, dan perbaikan sebelum lanjut. Jika keputusan teknis rutin dapat diambil dari spesifikasi ini, ambil keputusan yang paling sederhana dan dokumentasikan. Jangan menambah fitur di luar scope ketika alur utama belum stabil. Pekerjaan selesai ketika seluruh acceptance criteria yang dapat dieksekusi sudah terpenuhi dan blocker tersisa dijelaskan secara konkret. 

## **18 Prompt lanjutan per tahap** 

### **18.1 Membangun fondasi** 

Lanjutkan dari repository sekarang. Selesaikan audit Odoo 19 Community, Compose, database dev dan test, instalasi modul standar, company, lokasi, serta produk demo. Jalankan alur receipt 100 kg sampai MO standar sederhana. Berikan bukti versi dan perintah instalasi yang berhasil. Dashboard menunggu sampai transaksi dasar benar. 

### **18.2 Menyelesaikan core dan Manufacturing** 

Bangun keluarga material, metadata ukuran, measurement, ledger, dan security. Implementasikan baseline serta neraca produksi. Selesaikan MO A dengan keluaran 72 kg produk, 20 kg remnant, 6 kg scrap, dan loss 2 kg. Buktikan repeated completion tidak menggandakan stock atau ledger. Sertakan pengujian partial MO dan backorder. 

### **18.3 Menyelesaikan Waste Management** 

Bangun inspeksi, lokasi karantina, pencarian potongan, approval reuse, substitusi komponen, dan hubungan parent child. Konsumsi R1 8 kg pada MO B, hasilkan anak 2 kg serta scrap 0,5 kg. Buktikan operator tidak dapat memakai lot yang salah atau melebihi available. Selesaikan dispatch 4 kg beserta retur uji. 

### **18.4 Menyelesaikan laporan dan dashboard** 

Hitung stok akhir 16,5 kg dan seluruh neraca acuan dari transaksi nyata dalam database demo. Implementasikan historical snapshot, denominator nol, agregat weighted yield, filter periode Jakarta, drilldown, serta CSV. Sesudah graph dan pivot cocok, buat tampilan kartu OWL. Jangan memakai hasil hitung yang dihardcode. 

### **18.5 Memeriksa sebelum demo dan sidang** 

Audit implementasi terhadap specification dan T01 sampai T18. Jalankan install serta upgrade pada database bersih dan uji restore. Periksa source angka dashboard, ACL server, concurrency reservasi, posting ganda, correction, serta traceability R1 ke R1A. Lengkapi README dan traceability penelitian. Berikan daftar gap yang masih ada dengan dampaknya. 

26 

## **19 Menghubungkan sistem dengan laporan penelitian** 

### **19.1 Bukti yang dikumpulkan sejak awal** 

Mulai dengan wawancara penanggung jawab, alur proses nyata, contoh proyek dan gambar, catatan bahan, kondisi stok sisa, serta cara pengambilan keputusan penggunaan ulang atau penjualan. Rekam tanggal, jabatan narasumber, bukti dokumen, dan izin penggunaan data. Lakukan pengukuran stok awal sebelum migrasi agar jumlah fisik tidak sekadar mengikuti angka yang dimasukkan ke aplikasi. 

Untuk setiap proyek terpilih, kumpulkan kebutuhan bahan, konsumsi, keluaran massa material, remnant, scrap, kehilangan, WIP, serta perubahan desain. Setelah sistem berjalan, kumpulkan catatan transaksi dan pengujian. Data simulasi digunakan untuk validasi perangkat lunak, sedangkan analisis kondisi perusahaan menggunakan data lapangan yang dapat ditelusuri. 

### **19.2 Pemetaan laporan masing-masing** 

|**Bagian laporan**|**Firdaus**|**Feriangga**|
|---|---|---|
|Bab I|Masalah informasi serta tindak lanjut sisa<br>pelat|Masalah keterhubungan rencana, aktual, dan<br>hasil penggunaan bahan|
|Bab II|Circular Economy, MFA, waste<br>information, ERP, Quickstart|Circular Economy, efisiensi material, BoM,<br>Manufacturing, Quickstart|
|Bab III|Batas MFA, pengumpulan massa,<br>pengembangan, dan evaluasi|Unit MO, baseline, indikator yield,<br>pengembangan, dan evaluasi|
|Bab IV|Aliran sisa, fit gap, model piece, reuse,<br>disposition|Proses produksi, fit gap, baseline, konsumsi,<br>dan neraca|
|Bab V|Rekonsiliasi, traceability, dashboard, dan<br>uji pengguna|Rumus efisiensi, fungsi MO, dashboard, dan<br>uji pengguna|
|Bab VI|Jawaban atas tujuan dan batas manfaat<br>yang dibuktikan|Jawaban atas tujuan dan batas manfaat yang<br>dibuktikan|



### **19.3 Klaim yang boleh dibuat dari jenis evaluasi** 

Test integrasi membuktikan fungsi pada kondisi yang diuji. Pembandingan dashboard dengan data manual membuktikan ketepatan rumus pada dataset itu. UAT mendukung kesesuaian tugas serta penerimaan pengguna. Pengukuran waktu pencarian sebelum dan sesudah dapat menunjukkan perubahan waktu pada tugas yang sebanding. 

Klaim penurunan waste atau penghematan pembelian memerlukan periode pembanding dan kendali atas jenis proyek, volume, grade, serta revisi desain. Jika desain evaluasi belum memadai, hasil penelitian dinyatakan sebagai dukungan pencatatan dan evaluasi, disertai potensi manfaat yang belum dibuktikan. Pemakaian ulang dan efisiensi material tidak langsung membuktikan penurunan dampak lingkungan, karena evaluasi lingkungan mempunyai kebutuhan data tersendiri. 

27 

### **19.4 Posisi referensi yang dilampirkan** 

Enam PDF CE BAB 1 sampai CE BAB 6 menggambarkan TA modul warehouse pada PT Elco Indonesia Sejahtera menggunakan Odoo 16. Gunakan sebagai pembanding struktur analisis proses, fit gap, konfigurasi, dan pengujian. Alur penyamakan kulit, angka penelitian, struktur biaya, serta kesimpulan objek tersebut tidak dipindahkan menjadi fakta CV Teknika Prima Raya. Lengkapi identitas penulis dan judul dokumen jika akan mengutipnya dalam laporan formal. 

## **20 Rujukan dan sumber teknis** 

- CV Teknika Prima Raya. (Tanpa tahun). Company profile [Dokumen perusahaan]. Halaman tercetak 1, 8, dan 19. Sumber file yang dilampirkan pengguna. 

- Firdaus Al Hamid. (2026). Draf Bab I pengembangan Odoo modul Waste Management [Draf awal penelitian, 6 Oktober 2026]. Sumber konteks masalah awal, memerlukan validasi lapangan. 

- Allwood, J. M., Ashby, M. F., Gutowski, T. G., & Worrell, E. (2011). Material efficiency: A white paper. Resources, Conservation and Recycling, 55(3), 362-381. https://doi.org/10.1016/j.resconrec.2010.11.002. Naskah akses terbuka penulis https://web.mit.edu/ebm/www/Publications/MEWP_Res_Cons_Recycl_2011.pdf 

- Hagedorn, W., Greiff, K., & Pauliuk, S. (2024). An environmental assessment framework for circular steel products. Sustainable Production and Consumption, 49, 193-207. https://doi.org/10.1016/j.spc.2024.05.031. Teks terbuka https://publications.rwth-aachen.de/record/988971/files/988971.pdf 

- Lutfiah, D. P., Ridwan, A. Y., Hediyanto, U. Y. K. S., & Kusumahastuti, K. P. (2024). Pengembangan Sistem ERP Modul Inventory untuk Proses Penyimpanan Alat Medis pada Instalasi Kedokteran Nuklir RSHS dengan Metode Quickstart. Jurnal Indonesia: Manajemen Informatika dan Komunikasi, 5(1), 66-79. https://doi.org/10.35870/jimik.v5i1.433. Laman penerbit https://journal.stmiki.ac.id/index.php/jimik/article/view/433 

- Pourrahimian, P., Seyedzadeh, S., Arabi, B., Kahani, D., & Lotfian, S. (2026). Digital enablers of the circular economy: A systematic review of applications, barriers, and future directions. Journal of Manufacturing and Materials Processing, 10(4), 112. https://doi.org/10.3390/jmmp10040112. Teks terbuka https://strathprints.strath.ac.uk/95872/1/Pourrahimian-etal-JMMP-2026-Digital-enablers-of-the-circulareconomy.pdf 

- Safitri, N. K., Ridwan, A. Y., Hediyanto, U. Y. K. S., & Hadi, R. M. E. (2021). Developing Waste Management System based on Open-Source ERP. JATISI (Jurnal Teknik Informatika dan Sistem Informasi), 8(2), 848-858. https://doi.org/10.35957/jatisi.v8i2.915. Laman penerbit https://jurnal.mdp.ac.id/index.php/jatisi/article/view/1299 

- Odoo. (Tanpa tahun). By-Products. Odoo 19.0 documentation. 

https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/manufacturing/workflows/ byproducts.html. Diakses 11 Oktober 2026. 

- Odoo. (Tanpa tahun). Manufacturing source code branch 19.0. 

   - https://github.com/odoo/odoo/blob/19.0/addons/mrp/models/mrp_production.py. Diakses 11 Oktober 2026. 

- Odoo Community Association. (Tanpa tahun). Odoo web client UI related addons branch 19.0. https://github.com/OCA/web. Listing web_responsive versi 19.0.1.1.0. Diakses 11 Oktober 2026. 

28 

- Odoo Community Association. (Tanpa tahun). Odoo stock logistics workflow addons branch 19.0. https://github.com/OCA/stock-logistics-workflow. Listing stock_no_negative versi 19.0.1.0.0. Diakses 11 Oktober 2026. 

- Identitas dan DOI rujukan akademik dicocokkan dengan rekaman penerbit atau repositori penulis. Laman Lutfiah mengalami timeout dan PDF Safitri menolak akses pada pemeriksaan ini, sehingga pemakaiannya dibatasi pada informasi bibliografis serta topik penelitian yang terverifikasi. Unduh teks lengkap melalui penerbit sebelum menguraikan hasil, instrumen, atau detail tahapan kedua penelitian tersebut dalam Bab II. Definisi dan perhitungan sistem pada panduan ini merupakan spesifikasi usulan yang harus diuji, bukan salinan hasil penelitian terdahulu. 

29 

