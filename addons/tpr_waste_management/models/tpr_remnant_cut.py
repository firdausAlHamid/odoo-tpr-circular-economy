# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class TprRemnantCut(models.Model):
    _name = 'tpr.remnant.cut'
    _description = 'Catatan Sisa Potongan Pelat (Remnant / Scrap)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(
        string='Kode Potongan',
        required=True,
        copy=False,
        readonly=True,
        default='/',
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        default=lambda self: self.env.company,
        required=True
    )
    product_id = fields.Many2one(
        'product.product',
        string='Material / Produk Pelat',
        required=True,
        tracking=True,
        help='Material pelat induk asal potongan'
    )
    material_family_id = fields.Many2one(
        'tpr.material.family',
        string='Keluarga Material',
        related='product_id.material_family_id',
        store=True,
        readonly=True
    )
    material_grade_id = fields.Many2one(
        'tpr.material.grade',
        string='Grade Material',
        related='product_id.material_grade_id',
        store=True,
        readonly=True
    )
    material_thickness_id = fields.Many2one(
        'tpr.material.thickness',
        string='Ketebalan Nominal',
        related='product_id.material_thickness_id',
        store=True,
        readonly=True
    )

    # Dimensi Geometris (Metadata dalam mm)
    shape = fields.Selection([
        ('rectangle', 'Persegi Panjang (Rectangular)'),
        ('square', 'Bujur Sangkar (Square)'),
        ('triangle', 'Segitiga / Trapesium'),
        ('circle', 'Lingkaran / Flange Ring'),
        ('strip', 'Strip Panjang'),
        ('irregular', 'Tidak Beraturan (Irregular)'),
    ], string='Bentuk Geometri', default='rectangle', required=True, tracking=True,
       help='Bentuk fisik potongan pelat. Potongan tidak beraturan wajib diverifikasi secara manual.')

    length_mm = fields.Float(
        string='Panjang (mm)',
        required=True,
        digits=(10, 1),
        tracking=True,
        help='Dimensi panjang sisa potongan dalam milimeter'
    )
    width_mm = fields.Float(
        string='Lebar (mm)',
        required=True,
        digits=(10, 1),
        tracking=True,
        help='Dimensi lebar sisa potongan dalam milimeter'
    )
    thickness_mm = fields.Float(
        string='Tebal Aktual (mm)',
        required=True,
        digits=(6, 2),
        tracking=True,
        help='Ketebalan aktual hasil pengukuran dalam milimeter'
    )
    area_sqm = fields.Float(
        string='Luas Permukaan (m²)',
        compute='_compute_area_and_weight',
        store=True,
        digits=(10, 4)
    )

    # Massa Fisik (Satuan Inventaris kg)
    measurement_method = fields.Selection([
        ('scale', 'Timbangan Fisik Aktual (Weighed)'),
        ('calc_rect', 'Kalkulasi Teoretis Dimensi (Calculated)'),
        ('effective_area', 'Estimasi Luas Efektif Manual'),
    ], string='Metode Ukur Berat', default='scale', required=True, tracking=True,
       help='Metode penetapan berat. Timbangan aktual selalu diutamakan dibanding estimasi dimensi.')

    weight_kg = fields.Float(
        string='Berat Aktual (kg)',
        required=True,
        digits=(10, 3),
        tracking=True,
        help='Berat riil hasil penimbangan fisik dalam kilogram (kg)'
    )
    theoretical_weight_kg = fields.Float(
        string='Estimasi Berat Teoritis (kg)',
        compute='_compute_area_and_weight',
        store=True,
        digits=(10, 3),
        help='Estimasi berat teoritis berdasarkan formula massa jenis'
    )
    weight_deviation_pct = fields.Float(
        string='Deviasi Berat (%)',
        compute='_compute_weight_deviation',
        store=True,
        digits=(6, 2),
        help='Persentase selisih antara berat aktual penimbangan dengan estimasi teoretis pelat'
    )

    # Penelusuran Asal Transaksi & MO
    production_id = fields.Many2one(
        'mrp.production',
        string='Asal Manufacturing Order (MO)',
        copy=False,
        tracking=True,
        help='Manufacturing Order yang menghasilkan sisa potongan ini'
    )
    project_id = fields.Many2one(
        'project.project',
        string='Asal Proyek',
        copy=False,
        tracking=True,
        help='Proyek fabrikasi terkait'
    )
    parent_piece_id = fields.Many2one(
        'tpr.remnant.cut',
        string='Potongan Induk (Parent Piece)',
        copy=False,
        ondelete='set null',
        tracking=True,
        help='Potongan asal jika benda ini merupakan hasil pemotongan ulang dari potongan yang lebih besar'
    )
    child_piece_ids = fields.One2many(
        'tpr.remnant.cut',
        'parent_piece_id',
        string='Potongan Turunan (Child Pieces)',
        help='Daftar potongan anak yang dihasilkan dari pemotongan sisa ini'
    )
    source_stock_move_id = fields.Many2one(
        'stock.move',
        string='Transaksi Stok Masuk (By-Product / Penerimaan)',
        copy=False,
        readonly=True,
        help='Transaksi stock.move resmi yang mencatat pemasukan stok fisik potongan ini'
    )
    stock_lot_id = fields.Many2one(
        'stock.lot',
        string='Nomor Lot / Heat Number',
        domain="[('product_id', '=', product_id)]",
        help='Lot pelat induk untuk ketertelusuran material'
    )
    source_description = fields.Char(
        string='Identitas Komponen / Catatan Asal',
        help='Misal: Sisa pemotongan pelat base plate tangki T-102'
    )

    # Lokasi Fisik Persediaan
    location_id = fields.Many2one(
        'stock.location',
        string='Lokasi Stok Saat Ini',
        required=True,
        domain="[('usage', '=', 'internal')]",
        tracking=True,
        help='Lokasi fisik saat ini tempat potongan disimpan'
    )
    target_location_id = fields.Many2one(
        'stock.location',
        string='Lokasi Tujuan Relokasi',
        domain="[('usage', 'in', ('internal', 'inventory'))]",
        help='Lokasi tujuan bila potongan dipindahkan ke rak reusable atau area scrap fisik'
    )
    relocation_move_id = fields.Many2one(
        'stock.move',
        string='Transaksi Relokasi Stok',
        readonly=True,
        copy=False,
        help='Stock move resmi pemindahan lokasi'
    )

    # Status Karantina & Alur Pemeriksaan
    state = fields.Selection([
        ('draft', 'Draft / Baru Dicatat'),
        ('quarantine', 'Dalam Karantina'),
        ('inspected', 'Selesai Diperiksa'),
        ('cancelled', 'Dibatalkan'),
    ], string='Status Potongan', default='draft', required=True, tracking=True)

    inspection_result = fields.Selection([
        ('pending', 'Menunggu Penetapan'),
        ('reusable', 'Layak Digunakan Kembali (Reusable)'),
        ('scrap', 'Scrap Fisik (Untuk Dijual / Dilebur)'),
    ], string='Hasil Penetapan Petugas', default='pending', required=True, tracking=True)

    inspector_id = fields.Many2one(
        'res.users',
        string='Petugas Pemeriksa',
        readonly=True,
        copy=False,
        tracking=True
    )
    inspection_date = fields.Datetime(
        string='Waktu Pemeriksaan',
        readonly=True,
        copy=False,
        tracking=True
    )
    defect_type = fields.Selection([
        ('none', 'Tidak Ada Cacat Visual'),
        ('haz', 'Terkena Zona Panas / Heat-Affected Zone (HAZ)'),
        ('warped', 'Deformasi / Bengkok Sudut'),
        ('corrosion', 'Korosi / Karat Permukaan'),
        ('slag', 'Sisa Terak / Slag Pemotongan'),
        ('other', 'Kondisi Cacat Lainnya'),
    ], string='Kondisi Fisik / Cacat', default='none', tracking=True)

    inspection_notes = fields.Text(
        string='Catatan Hasil Evaluasi Petugas',
        help='Catatan rinci kondisi geometri, cacat visual, dan hasil uji'
    )
    reuse_reason = fields.Text(
        string='Rencana Penggunaan / Justifikasi',
        help='Alasan penetapan kelayakan atau rencana komponen yang dapat dibuat dari potongan ini'
    )

    is_simulation = fields.Boolean(
        string='Data Simulasi',
        default=False,
        help='Centang jika data ini dibuat untuk simulasi pengujian sistem dan bukan data riil pabrik'
    )

    @api.depends('length_mm', 'width_mm', 'thickness_mm', 'material_family_id.density')
    def _compute_area_and_weight(self):
        for rec in self:
            if rec.length_mm and rec.width_mm:
                rec.area_sqm = (rec.length_mm * rec.width_mm) / 1000000.0
            else:
                rec.area_sqm = 0.0

            density = rec.material_family_id.density or 7.85
            if rec.length_mm and rec.width_mm and rec.thickness_mm and density:
                rec.theoretical_weight_kg = (rec.length_mm * rec.width_mm * rec.thickness_mm * density) / 1000000.0
            else:
                rec.theoretical_weight_kg = 0.0

    @api.depends('weight_kg', 'theoretical_weight_kg')
    def _compute_weight_deviation(self):
        for rec in self:
            if rec.theoretical_weight_kg and rec.weight_kg:
                rec.weight_deviation_pct = ((rec.weight_kg - rec.theoretical_weight_kg) / rec.theoretical_weight_kg) * 100.0
            else:
                rec.weight_deviation_pct = 0.0

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            if self.product_id.nominal_thickness_mm and not self.thickness_mm:
                self.thickness_mm = self.product_id.nominal_thickness_mm

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                seq = self.env['ir.sequence'].next_by_code('tpr.remnant.cut')
                vals['name'] = seq or '/'
        return super().create(vals_list)

    def _compute_display_name(self):
        for rec in self:
            prod_name = rec.product_id.name if rec.product_id else 'Material'
            rec.display_name = f"[{rec.name}] {prod_name} ({rec.length_mm:.0f}x{rec.width_mm:.0f}x{rec.thickness_mm:.1f} mm)"

    # Actions Workflow
    def action_send_to_quarantine(self):
        for rec in self:
            if rec.weight_kg <= 0:
                raise UserError(_("Berat potongan aktual harus lebih dari 0 kg!"))
            if rec.length_mm <= 0 or rec.width_mm <= 0 or rec.thickness_mm <= 0:
                raise UserError(_("Dimensi panjang, lebar, dan tebal harus bernilai positif!"))
            rec.write({
                'state': 'quarantine',
                'inspection_result': 'pending',
            })
            rec.message_post(body=_("Potongan telah dipindahkan ke status Karantina untuk inspeksi fisik."))

    def action_approve_reuse(self):
        """Penetapan kelayakan reuse oleh petugas berwenang (bukan otomatis dari ukuran)."""
        if not self.env.su and not self.env.user.has_group('tpr_waste_management.group_tpr_waste_manager'):
            raise UserError(_("Hanya Petugas Pemeriksa / Penanggung Jawab yang berwenang menetapkan kelayakan reusable!"))
        for rec in self:
            vals = {
                'state': 'inspected',
                'inspection_result': 'reusable',
                'inspector_id': self.env.user.id,
                'inspection_date': fields.Datetime.now(),
            }
            if not rec.target_location_id:
                reusable_loc = self.env.ref('tpr_waste_management.location_tpr_reusable_rack', raise_if_not_found=False)
                if not reusable_loc:
                    reusable_loc = self.env['stock.location'].search([
                        ('name', 'ilike', 'reusable'),
                        ('usage', '=', 'internal'),
                        ('company_id', 'in', (False, rec.company_id.id))
                    ], limit=1)
                if reusable_loc:
                    vals['target_location_id'] = reusable_loc.id
            rec.write(vals)
            rec.message_post(body=_("Potongan diverifikasi dan disetujui sebagai **Layak Digunakan Kembali (Reusable)** oleh %s.") % self.env.user.name)

    def action_reject_to_scrap(self):
        """Penetapan sisa sebagai scrap fisik oleh petugas berwenang."""
        if not self.env.su and not self.env.user.has_group('tpr_waste_management.group_tpr_waste_manager'):
            raise UserError(_("Hanya Petugas Pemeriksa / Penanggung Jawab yang berwenang menetapkan status Scrap!"))
        for rec in self:
            vals = {
                'state': 'inspected',
                'inspection_result': 'scrap',
                'inspector_id': self.env.user.id,
                'inspection_date': fields.Datetime.now(),
            }
            if not rec.target_location_id:
                scrap_loc = self.env.ref('tpr_waste_management.location_tpr_physical_scrap', raise_if_not_found=False)
                if not scrap_loc:
                    scrap_loc = self.env['stock.location'].search([
                        ('name', 'ilike', 'scrap'),
                        ('usage', '=', 'internal'),
                        ('company_id', 'in', (False, rec.company_id.id))
                    ], limit=1)
                if scrap_loc:
                    vals['target_location_id'] = scrap_loc.id
            rec.write(vals)
            rec.message_post(body=_("Potongan ditetapkan sebagai **Scrap Fisik** oleh %s.") % self.env.user.name)

    def action_reset_to_draft(self):
        for rec in self:
            rec.write({
                'state': 'draft',
                'inspection_result': 'pending',
            })

    def action_cancel(self):
        for rec in self:
            rec.write({'state': 'cancelled'})

    def action_execute_relocation(self):
        """
        Memindahkan stok fisik potongan ke lokasi baru secara standar menggunakan stock.move resmi,
        tanpa mengubah saldo stock.quant secara langsung.
        """
        self.ensure_one()
        if not self.target_location_id:
            raise UserError(_("Pilih 'Lokasi Tujuan Relokasi' terlebih dahulu!"))
        if self.target_location_id == self.location_id:
            raise UserError(_("Lokasi tujuan sama dengan lokasi saat ini!"))
        if self.weight_kg <= 0:
            raise UserError(_("Berat potongan tidak valid untuk perpindahan inventaris."))

        # Buat transaksi perpindahan inventaris standar
        StockMove = self.env['stock.move']
        move_vals = {
            'description_picking': _("Relokasi Potongan: %s (%s)") % (self.name, self.inspection_result),
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_id.id,
            'product_uom_qty': self.weight_kg,
            'location_id': self.location_id.id,
            'location_dest_id': self.target_location_id.id,
            'company_id': self.company_id.id,
            'origin': self.name,
        }
        move = StockMove.create(move_vals)
        move._action_confirm()
        # Isi kuantitas aktual perpindahan
        move.quantity = self.weight_kg
        move.picked = True
        if self.stock_lot_id and move.move_line_ids:
            move.move_line_ids.write({'lot_id': self.stock_lot_id.id})
        move._action_done()

        # Update lokasi potongan dan simpan referensi move resmi
        old_loc_name = self.location_id.display_name
        self.write({
            'location_id': self.target_location_id.id,
            'relocation_move_id': move.id,
        })
        self.message_post(body=_("Stok potongan seberat %s kg berhasil dipindahkan dari %s ke %s via Stock Move %s.") % (
            self.weight_kg, old_loc_name, self.target_location_id.display_name, move.reference or move.origin or self.name
        ))
        return True
