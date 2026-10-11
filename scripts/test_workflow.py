"""Test end-to-end Circular Core & Waste Management workflow on database tpr_test."""
import os
import sys
import odoo
from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry

def run_test():
    args = [
        '-c', '/etc/odoo/odoo.conf',
        '-d', 'tpr_test',
        f'--db_host={os.environ.get("HOST", "db")}',
        f'--db_port={os.environ.get("PORT", "5432")}',
        f'--db_user={os.environ.get("USER", "odoo")}',
        f'--db_password={os.environ.get("PASSWORD", "")}',
    ]
    odoo.tools.config.parse_config(args)
    registry = Registry('tpr_test')

    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        print("=== 1. VERIFIKASI MASTER DATA CIRCULAR CORE ===")
        families = env['tpr.material.family'].search([])
        grades = env['tpr.material.grade'].search([])
        thicknesses = env['tpr.material.thickness'].search([])
        print(f"Keluarga Material: {[f.name for f in families]} (Total: {len(families)})")
        print(f"Grade Material: {[g.display_name for g in grades]} (Total: {len(grades)})")
        print(f"Ketebalan Nominal: {[t.name for t in thicknesses]} (Total: {len(thicknesses)})")
        assert len(families) >= 3, "Harus ada minimal 3 keluarga material!"
        assert len(grades) >= 3, "Harus ada minimal 3 grade material!"
        assert len(thicknesses) >= 5, "Harus ada minimal 5 ketebalan material!"

        print("\n=== 2. VERIFIKASI LOKASI STOK SIRKULARITAS ===")
        loc_quarantine = env.ref('tpr_waste_management.location_tpr_quarantine')
        loc_reusable = env.ref('tpr_waste_management.location_tpr_reusable_rack')
        loc_scrap = env.ref('tpr_waste_management.location_tpr_physical_scrap')
        print(f"Lokasi Karantina: {loc_quarantine.complete_name}")
        print(f"Lokasi Rak Reusable: {loc_reusable.complete_name}")
        print(f"Lokasi Scrap Fisik: {loc_scrap.complete_name}")

        print("\n=== 3. VERIFIKASI PRODUK PELAT & METADATA ===")
        product_6mm = env.ref('tpr_waste_management.product_plate_ss400_6mm')
        assert product_6mm.is_plate_material, "Produk harus berstatus material pelat!"
        assert product_6mm.uom_id.name == 'kg', "Satuan stok harus kg!"
        calc_wt = product_6mm.calculate_theoretical_weight_kg(1000.0, 500.0, 6.0)
        # 1000 * 500 * 6 * 7.85 / 1000000 = 23.55 kg
        print(f"Produk Pelat: {product_6mm.name} (Stok UoM: {product_6mm.uom_id.name})")
        print(f"Perhitungan teoritis 1000x500x6 mm: {calc_wt:.2f} kg (Ekspektasi: 23.55 kg)")
        assert abs(calc_wt - 23.55) < 0.01, f"Perhitungan massa salah: {calc_wt}"

        print("\n=== 4. SIMULASI TRANSAKSI PRODUKSI (MO) DENGAN BY-PRODUCT FISIK ===")
        # Buat MO sederhana untuk fabrikasi
        stock_loc = env.ref('stock.stock_location_stock')
        uom_kg = env.ref('uom.product_uom_kgm')

        # Siapkan saldo awal bahan baku pelat di stock_location via Inventory Adjustment / standard Move
        # Gunakan stock.move standar untuk mengisi saldo bahan
        supp_loc = env.ref('stock.stock_location_suppliers')
        init_move = env['stock.move'].create({
            'description_picking': 'Penerimaan Bahan Baku Pelat (Simulasi)',
            'product_id': product_6mm.id,
            'product_uom': uom_kg.id,
            'product_uom_qty': 100.0,
            'location_id': supp_loc.id,
            'location_dest_id': stock_loc.id,
            'company_id': env.company.id,
            'origin': 'SIM-RECEIPT-01',
        })
        init_move._action_confirm()
        init_move.quantity = 100.0
        init_move.picked = True
        init_move._action_done()
        print(f"Pemasukan awal bahan baku pelat: 100 kg selesai via move {init_move.reference or init_move.origin}")

        # Buat MO fabrikasi
        mo = env['mrp.production'].create({
            'product_id': product_6mm.id,
            'product_qty': 60.0,  # 60 kg produk jadi
            'product_uom_id': uom_kg.id,
            'location_src_id': stock_loc.id,
            'location_dest_id': stock_loc.id,
            'company_id': env.company.id,
        })
        # Tambahkan pemakaian bahan baku 100 kg
        env['stock.move'].create({
            'description_picking': 'Konsumsi Pelat Induk',
            'raw_material_production_id': mo.id,
            'product_id': product_6mm.id,
            'product_uom': uom_kg.id,
            'product_uom_qty': 100.0,
            'location_id': stock_loc.id,
            'location_dest_id': env.ref('stock.stock_location_components').id if env.ref('stock.stock_location_components', False) else stock_loc.id,
            'company_id': env.company.id,
        })
        # Tambahkan by-product fisik 40 kg yang diarahkan ke Karantina Sisa Produksi!
        byproduct_move = env['stock.move'].create({
            'description_picking': 'By-Product Sisa Potongan Pelat',
            'production_id': mo.id,
            'product_id': product_6mm.id,
            'product_uom': uom_kg.id,
            'product_uom_qty': 40.0,
            'location_id': env.ref('stock.stock_location_components').id if env.ref('stock.stock_location_components', False) else stock_loc.id,
            'location_dest_id': loc_quarantine.id,
            'company_id': env.company.id,
        })
        mo.action_confirm()
        print(f"Manufacturing Order {mo.name} dikonfirmasi dengan 1 Finished (60 kg) dan 1 By-Product (40 kg di Karantina).")

        # Selesaikan MO
        mo.button_mark_done()
        print(f"MO {mo.name} selesai. State: {mo.state}")

        print("\n=== 5. PENCATATAN POTONGAN REMNANT & ALUR KARANTINA ===")
        # Potongan 1: Remnant 30 kg
        remnant_1 = env['tpr.remnant.cut'].create({
            'product_id': product_6mm.id,
            'length_mm': 1600.0,
            'width_mm': 800.0,
            'thickness_mm': 6.0,
            'weight_kg': 30.0,
            'location_id': loc_quarantine.id,
            'production_id': mo.id,
            'source_stock_move_id': byproduct_move.id,
            'source_description': f"Sisa pelat pemotongan MO {mo.name}",
            'is_simulation': True,
        })
        print(f"Potongan 1 dibuat: {remnant_1.name} ({remnant_1.length_mm}x{remnant_1.width_mm}x{remnant_1.thickness_mm} mm, {remnant_1.weight_kg} kg)")
        print(f"Status awal: {remnant_1.state}, Hasil inspeksi: {remnant_1.inspection_result}")

        # Masuk karantina
        remnant_1.action_send_to_quarantine()
        assert remnant_1.state == 'quarantine', "State harus quarantine!"
        print(f"Potongan 1 dipindahkan ke karantina: State = {remnant_1.state}")

        # Buat atau ambil user operator biasa dan inspector untuk uji hak akses
        grp_user = env.ref('tpr_waste_management.group_tpr_waste_user')
        grp_mgr = env.ref('tpr_waste_management.group_tpr_waste_manager')
        operator_user = env['res.users'].search([('login', '=', 'budi_operator_sim')], limit=1)
        if not operator_user:
            operator_user = env['res.users'].create({
                'name': 'Budi Operator (Simulasi)',
                'login': 'budi_operator_sim',
                'email': 'budi@example.com',
                'group_ids': [(6, 0, [grp_user.id])],
            })
        inspector_user = env['res.users'].search([('login', '=', 'daus_inspector_sim')], limit=1)
        if not inspector_user:
            inspector_user = env['res.users'].create({
                'name': 'Daus Inspector (Simulasi)',
                'login': 'daus_inspector_sim',
                'email': 'daus@example.com',
                'group_ids': [(6, 0, [grp_mgr.id])],
            })

        # Uji hak akses: Operator biasa tidak boleh menyetujui reuse
        try:
            remnant_1.with_user(operator_user).action_approve_reuse()
            raise AssertionError("Harus gagal: Operator biasa tidak boleh menyetujui reuse!")
        except odoo.exceptions.UserError as e:
            print(f"Verifikasi Hak Akses: Operator biasa berhasil dicegah menyetujui reuse ({e})")

        # Inspeksi dan penetapan REUSABLE oleh inspector yang berwenang
        remnant_1.write({
            'shape': 'rectangle',
            'measurement_method': 'scale',
            'inspection_notes': 'Kondisi pelat lurus, pemotongan rapi tanpa cacat termal HAZ.',
            'reuse_reason': 'Dapat digunakan untuk fabrikasi bracket pada proyek berikutnya.',
        })
        remnant_1.with_user(inspector_user).action_approve_reuse()
        assert remnant_1.state == 'inspected', "State harus inspected!"
        assert remnant_1.inspection_result == 'reusable', "Hasil harus reusable!"
        assert remnant_1.target_location_id == loc_reusable, "Target location harus otomatis disarankan ke Rak Reusable!"
        print(f"Potongan 1 disetujui Reusable oleh {remnant_1.inspector_id.name} pada {remnant_1.inspection_date}")
        print(f"Auto-suggest target location: {remnant_1.target_location_id.complete_name}")

        # Relokasi fisik stok ke Rak Remnant Reusable menggunakan stock.move resmi
        remnant_1.action_execute_relocation()
        assert remnant_1.location_id == loc_reusable, "Lokasi harus pindah ke Rak Reusable!"
        assert remnant_1.relocation_move_id, "Relocation move id harus tercatat!"
        print(f"Relokasi stok Potongan 1 selesai: Lokasi baru = {remnant_1.location_id.name}, Move = {remnant_1.relocation_move_id.reference or remnant_1.relocation_move_id.origin}")

        print("\n=== 6. PENCATATAN POTONGAN SCRAP FISIK (OFFCUT KECIL) ===")
        # Potongan 2: Scrap sisa 10 kg
        remnant_2 = env['tpr.remnant.cut'].create({
            'product_id': product_6mm.id,
            'shape': 'irregular',
            'measurement_method': 'scale',
            'length_mm': 400.0,
            'width_mm': 150.0,
            'thickness_mm': 6.0,
            'weight_kg': 10.0,
            'location_id': loc_quarantine.id,
            'production_id': mo.id,
            'source_stock_move_id': byproduct_move.id,
            'source_description': f"Offcut potongan tepi MO {mo.name}",
            'is_simulation': True,
        })
        remnant_2.action_send_to_quarantine()
        remnant_2.write({
            'defect_type': 'slag',
            'inspection_notes': 'Ukuran terlalu kecil dan banyak terak las/plasma.',
            'reuse_reason': 'Tidak layak struktural, disimpan di area scrap untuk ditimbang dan dijual kiloan.',
        })
        remnant_2.with_user(inspector_user).action_reject_to_scrap()
        assert remnant_2.inspection_result == 'scrap', "Hasil harus scrap!"
        assert remnant_2.target_location_id == loc_scrap, "Target location harus otomatis disarankan ke Area Scrap Fisik!"
        print(f"Potongan 2 ditetapkan Scrap Fisik oleh {remnant_2.inspector_id.name}")
        print(f"Auto-suggest target location: {remnant_2.target_location_id.complete_name}")

        # Relokasi ke Area Scrap Fisik via stock.move standar
        remnant_2.action_execute_relocation()
        assert remnant_2.location_id == loc_scrap, "Lokasi harus pindah ke Area Scrap!"
        print(f"Relokasi stok Potongan 2 selesai: Lokasi baru = {remnant_2.location_id.name}, Move = {remnant_2.relocation_move_id.reference or remnant_2.relocation_move_id.origin}")

        print("\n=== 7. PENGUJIAN HUBUNGAN POTONGAN INDUK - ANAK (PARENT - CHILD TRACEABILITY) ===")
        # Potongan 3: Sisa strip hasil pemotongan ulang dari Potongan 1 (Remnant Induk)
        remnant_child = env['tpr.remnant.cut'].create({
            'product_id': product_6mm.id,
            'parent_piece_id': remnant_1.id,
            'shape': 'strip',
            'measurement_method': 'scale',
            'length_mm': 1600.0,
            'width_mm': 200.0,
            'thickness_mm': 6.0,
            'weight_kg': 7.5,
            'location_id': loc_reusable.id,
            'production_id': mo.id,  # Tetap mewarisi asal MO pertama
            'source_description': f"Potongan strip sisa pemotongan ulang dari {remnant_1.name}",
            'is_simulation': True,
        })
        assert remnant_child.parent_piece_id == remnant_1, "Parent piece harus merujuk ke Potongan 1!"
        assert remnant_child in remnant_1.child_piece_ids, "Potongan anak harus ada di daftar child_piece_ids induk!"
        print(f"Potongan Anak dibuat: {remnant_child.name} (Parent: {remnant_child.parent_piece_id.name})")
        print(f"Daftar anak dari {remnant_1.name}: {[c.name for c in remnant_1.child_piece_ids]}")

        # Verifikasi smart button di MO
        assert mo.remnant_count >= 2, f"MO harus memiliki minimal 2 potongan terkait, ditemukan {mo.remnant_count}"
        print(f"\nVerifikasi MO {mo.name}: memiliki {mo.remnant_count} catatan sisa potongan terhubung.")

        print("\n=== 8. PENGUJIAN VISUALISASI DIAGRAM SANKEY MFA ===")
        # 8.1 Test Benchmark MO A
        mfa_a = env['tpr.mfa.analysis'].create({
            'name': 'Uji Diagram Sankey MO A (100 kg)',
            'production_id': mo.id,
        })
        mfa_a.action_load_demo_benchmark()
        assert mfa_a.total_input_kg == 100.0, "Total input harus 100 kg!"
        assert mfa_a.yield_pct == 72.0, "Yield harus 72.0%!"
        assert mfa_a.remnant_pct == 20.0, "Remnant harus 20.0%!"
        assert mfa_a.scrap_pct == 6.0, "Scrap harus 6.0%!"
        assert mfa_a.loss_pct == 2.0, "Loss harus 2.0%!"
        assert mfa_a.residual_kg == 0.0, "Residual harus seimbang 0.0 kg!"
        svg_a = mfa_a._generate_sankey_svg()
        assert 'Model Sirkularitas Almaty' in svg_a, "Harus mengacu model Almaty!"
        assert 'alm-ribbon' in svg_a, "Harus memiliki pita aliran alm-ribbon!"
        assert 'PELAT BARU (I_baru)' in svg_a, "Harus ada label input!"
        assert 'PRODUK JADI (P)' in svg_a, "Harus ada label output produk!"
        assert 'CYCLED RESOURCES' in svg_a, "Harus ada siklus sirkularitas Cycled Resources!"
        print(f"Sankey MO A terverifikasi: Total {mfa_a.total_input_kg} kg, Yield {mfa_a.yield_pct}%, SVG length {len(svg_a)}")

        # 8.2 Test Pemakaian Ulang MO B
        mfa_b = env['tpr.mfa.analysis'].create({
            'name': 'Uji Diagram Sankey MO B (8 kg Reuse)',
        })
        mfa_b.action_load_demo_reuse()
        assert mfa_b.reused_input_kg == 8.0, "Input reused harus 8 kg!"
        assert mfa_b.reused_input_pct == 100.0, "Input reused pct harus 100%!"
        assert mfa_b.yield_pct == 68.75, "Yield MO B harus 68.75%!"
        svg_b = mfa_b._generate_sankey_svg()
        assert 'INPUT REMNANT (I_ulang)' in svg_b, "Harus ada label input remnant!"
        print(f"Sankey MO B terverifikasi: Reused {mfa_b.reused_input_kg} kg, Yield {mfa_b.yield_pct}%, SVG length {len(svg_b)}")

        print("\n=== SEMUA PENGUJIAN ALUR DASAR & DIAGRAM SANKEY BERHASIL LOLOS 100%! ===")

if __name__ == '__main__':
    run_test()
