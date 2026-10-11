# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TprMfaAnalysis(models.Model):
    _name = 'tpr.mfa.analysis'
    _description = 'Material Flow Analysis (MFA) & Sankey Diagram'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(
        string='Judul Analisis MFA',
        required=True,
        default='Analisis Aliran Massa Pelat',
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        default=lambda self: self.env.company,
        required=True
    )
    material_family_id = fields.Many2one(
        'tpr.material.family',
        string='Keluarga Material',
        required=True,
        default=lambda self: self.env['tpr.material.family'].search([], limit=1),
        help='Keluarga material pelat yang menjadi batas neraca massa'
    )
    production_id = fields.Many2one(
        'mrp.production',
        string='Manufacturing Order (MO)',
        help='Pilih MO spesifik untuk menarik data pemakaian dan sisa potongan aktual'
    )
    analysis_date = fields.Date(
        string='Tanggal Analisis',
        default=fields.Date.context_today,
        required=True
    )
    notes = fields.Text(
        string='Catatan Evaluasi / Bukti Pengukuran',
        help='Catatan metode pengukuran massa, toleransi timbangan, atau alasan selisih neraca'
    )

    # Masukan Massa (Inputs)
    raw_input_kg = fields.Float(
        string='Masukan Bahan Baru (I_baru)',
        default=100.0,
        digits=(10, 2),
        tracking=True,
        help='Massa pelat baru yang diambil dari gudang bahan baku (kg)'
    )
    reused_input_kg = fields.Float(
        string='Masukan Potongan Ulang (I_ulang)',
        default=0.0,
        digits=(10, 2),
        tracking=True,
        help='Massa potongan sisa (remnant) yang digunakan kembali sebagai bahan masukan (kg)'
    )
    total_input_kg = fields.Float(
        string='Total Masukan Proses (D)',
        compute='_compute_balance_and_indicators',
        store=True,
        digits=(10, 2),
        help='Total massa material yang diproses: D = I_baru + I_ulang'
    )

    # Keluaran Massa (Outputs)
    product_output_kg = fields.Float(
        string='Massa pada Produk Jadi (P)',
        default=72.0,
        digits=(10, 2),
        tracking=True,
        help='Massa pelat yang terkandung dalam komponen atau produk jadi (kg)'
    )
    remnant_output_kg = fields.Float(
        string='Sisa Potongan Reusable (R)',
        default=20.0,
        digits=(10, 2),
        tracking=True,
        help='Massa potongan sisa yang layak digunakan kembali dan disimpan di rak (kg)'
    )
    scrap_output_kg = fields.Float(
        string='Scrap Fisik (S)',
        default=6.0,
        digits=(10, 2),
        tracking=True,
        help='Massa offcut kecil/rusak yang dialokasikan ke area scrap fisik untuk dijual (kg)'
    )
    loss_kg = fields.Float(
        string='Kehilangan Proses / Kerf (L)',
        default=2.0,
        digits=(10, 2),
        tracking=True,
        help='Massa material yang hilang akibat lebar celah pemotongan (kerf loss) atau debu plasma/gerinda (kg)'
    )
    residual_kg = fields.Float(
        string='Residual / Selisih Neraca (e)',
        compute='_compute_balance_and_indicators',
        store=True,
        digits=(10, 2),
        help='Selisih neraca massa belum terjelaskan: e = D - (P + R + S + L)'
    )

    # Indikator Efisiensi (%)
    yield_pct = fields.Float(
        string='Yield Material (%)',
        compute='_compute_balance_and_indicators',
        store=True,
        digits=(6, 2),
        help='Rasio massa produk terhadap total masukan proses: (P / D) * 100%'
    )
    remnant_pct = fields.Float(
        string='Proporsi Remnant (%)',
        compute='_compute_balance_and_indicators',
        store=True,
        digits=(6, 2),
        help='(R / D) * 100%'
    )
    scrap_pct = fields.Float(
        string='Proporsi Scrap (%)',
        compute='_compute_balance_and_indicators',
        store=True,
        digits=(6, 2),
        help='(S / D) * 100%'
    )
    loss_pct = fields.Float(
        string='Proporsi Kehilangan (%)',
        compute='_compute_balance_and_indicators',
        store=True,
        digits=(6, 2),
        help='(L / D) * 100%'
    )
    reused_input_pct = fields.Float(
        string='Proporsi Input Ulang (%)',
        compute='_compute_balance_and_indicators',
        store=True,
        digits=(6, 2),
        help='(I_ulang / D) * 100%'
    )

    # Visualisasi Diagram Sankey
    sankey_chart_html = fields.Html(
        string='Diagram Aliran Massa (Sankey)',
        compute='_compute_sankey_chart',
        sanitize=False
    )

    @api.depends('raw_input_kg', 'reused_input_kg', 'product_output_kg', 'remnant_output_kg', 'scrap_output_kg', 'loss_kg')
    def _compute_balance_and_indicators(self):
        for rec in self:
            rec.total_input_kg = rec.raw_input_kg + rec.reused_input_kg
            total_out = rec.product_output_kg + rec.remnant_output_kg + rec.scrap_output_kg + rec.loss_kg
            rec.residual_kg = rec.total_input_kg - total_out

            d = rec.total_input_kg
            if d > 0:
                rec.yield_pct = (rec.product_output_kg / d) * 100.0
                rec.remnant_pct = (rec.remnant_output_kg / d) * 100.0
                rec.scrap_pct = (rec.scrap_output_kg / d) * 100.0
                rec.loss_pct = (rec.loss_kg / d) * 100.0
                rec.reused_input_pct = (rec.reused_input_kg / d) * 100.0
            else:
                rec.yield_pct = 0.0
                rec.remnant_pct = 0.0
                rec.scrap_pct = 0.0
                rec.loss_pct = 0.0
                rec.reused_input_pct = 0.0

    @api.depends('raw_input_kg', 'reused_input_kg', 'total_input_kg',
                 'product_output_kg', 'remnant_output_kg', 'scrap_output_kg', 'loss_kg', 'residual_kg')
    def _compute_sankey_chart(self):
        for rec in self:
            rec.sankey_chart_html = rec._generate_sankey_svg()

    def _generate_sankey_svg(self):
        """
        Menghasilkan kode SVG responsif, proporsional, dan estetik untuk Diagram Sankey MFA
        mengacu pada metodologi visualisasi Almaty / Circle Economy (Metabolic MFA Standard):
        - Latar belakang bersih (Clean White / Light aesthetic).
        - Setiap node berupa kartu/badge mandiri bergaya Almaty dengan ikon, judul kategori, dan angka bobot tebal.
        - Spacing vertikal antar-kartu keluaran dijamin minimal 20-25px, sehingga secara matematis MUSTAHIL terjadi teks tumpang-tindih (overlap).
        - Pita aliran halus (Smooth S-Curve Bezier Ribbons) dengan gradien warna modern.
        - Jalur Sirkularitas Remnant (Cycled Resources) melengkung elegan di bagian atas (Top Highway Loop) dengan marka arah.
        """
        d = self.total_input_kg if self.total_input_kg > 0 else 1.0
        raw_val = max(0.0, self.raw_input_kg)
        reused_val = max(0.0, self.reused_input_kg)
        p_val = max(0.0, self.product_output_kg)
        r_val = max(0.0, self.remnant_output_kg)
        s_val = max(0.0, self.scrap_output_kg)
        l_val = max(0.0, self.loss_kg)
        res_val = max(0.0, self.residual_kg)

        # Dimensi Canvas SVG
        svg_w, svg_h = 1140, 540

        # Koordinat Kartu Node
        # Kolom Masukan (Input Cards)
        card_in_x = 110.0
        card_in_w = 180.0
        card_in_h = 54.0

        y_card_raw = 165.0
        y_card_reused = 255.0

        # Kolom Pemrosesan (Center Process Card)
        proc_x = 475.0
        proc_w = 190.0
        proc_h = 170.0
        proc_y = 185.0

        # Kolom Keluaran (Output Cards)
        card_out_x = 855.0
        card_out_w = 180.0
        card_out_h = 52.0

        # Penataan Y Kartu Keluaran dengan Jarak Aman Permanen (Guaranteed Zero Overlap)
        y_out_p = 135.0
        y_out_r = 210.0
        y_out_s = 285.0
        y_out_l = 360.0
        y_out_res = 435.0

        # Fungsi pembuat kurva Bezier pita aliran halus (Smooth S-Curve Ribbon)
        def make_ribbon(x1, y1_top, h1, x2, y2_top, h2):
            y1_bot = y1_top + max(3.0, h1)
            y2_bot = y2_top + max(3.0, h2)
            dx = x2 - x1
            cx1 = x1 + dx * 0.5
            cx2 = x2 - dx * 0.5
            return (
                f"M {x1:.1f} {y1_top:.1f} "
                f"C {cx1:.1f} {y1_top:.1f}, {cx2:.1f} {y2_top:.1f}, {x2:.1f} {y2_top:.1f} "
                f"L {x2:.1f} {y2_bot:.1f} "
                f"C {cx2:.1f} {y2_bot:.1f}, {cx1:.1f} {y1_bot:.1f}, {x1:.1f} {y1_bot:.1f} Z"
            )

        # 1. Pita Aliran Masukan ke Pemrosesan
        h_proc_raw = (raw_val / d) * proc_h
        h_proc_reused = (reused_val / d) * proc_h

        h_in_raw_ribbon = max(10.0, min(38.0, (raw_val / d) * 44.0)) if raw_val > 0 else 0
        h_in_reused_ribbon = max(10.0, min(38.0, (reused_val / d) * 44.0)) if reused_val > 0 else 0

        ribbon_raw = ""
        if raw_val > 0:
            ribbon_raw = make_ribbon(
                card_in_x + card_in_w, y_card_raw + 27 - h_in_raw_ribbon / 2, h_in_raw_ribbon,
                proc_x, proc_y, h_proc_raw
            )

        ribbon_reused = ""
        if reused_val > 0:
            ribbon_reused = make_ribbon(
                card_in_x + card_in_w, y_card_reused + 27 - h_in_reused_ribbon / 2, h_in_reused_ribbon,
                proc_x, proc_y + h_proc_raw, h_proc_reused
            )

        # 2. Pita Aliran Pemrosesan ke Keluaran
        curr_proc_y = proc_y

        # Produk Jadi
        h_proc_p = (p_val / d) * proc_h
        h_out_p = max(8.0, min(38.0, (p_val / d) * 44.0)) if p_val > 0 else 0
        ribbon_p = ""
        if p_val > 0:
            ribbon_p = make_ribbon(
                proc_x + proc_w, curr_proc_y, h_proc_p,
                card_out_x, y_out_p + 26 - h_out_p / 2, h_out_p
            )
            curr_proc_y += h_proc_p

        # Remnant Reusable
        h_proc_r = (r_val / d) * proc_h
        h_out_r = max(8.0, min(36.0, (r_val / d) * 44.0)) if r_val > 0 else 0
        ribbon_r = ""
        if r_val > 0:
            ribbon_r = make_ribbon(
                proc_x + proc_w, curr_proc_y, h_proc_r,
                card_out_x, y_out_r + 26 - h_out_r / 2, h_out_r
            )
            curr_proc_y += h_proc_r

        # Scrap Fisik
        h_proc_s = (s_val / d) * proc_h
        h_out_s = max(6.0, min(34.0, (s_val / d) * 44.0)) if s_val > 0 else 0
        ribbon_s = ""
        if s_val > 0:
            ribbon_s = make_ribbon(
                proc_x + proc_w, curr_proc_y, h_proc_s,
                card_out_x, y_out_s + 26 - h_out_s / 2, h_out_s
            )
            curr_proc_y += h_proc_s

        # Kehilangan Proses (Kerf)
        h_proc_l = (l_val / d) * proc_h
        h_out_l = max(5.0, min(32.0, (l_val / d) * 44.0)) if l_val > 0 else 0
        ribbon_l = ""
        if l_val > 0:
            ribbon_l = make_ribbon(
                proc_x + proc_w, curr_proc_y, h_proc_l,
                card_out_x, y_out_l + 26 - h_out_l / 2, h_out_l
            )
            curr_proc_y += h_proc_l

        # Residual (Jika ada selisih)
        ribbon_res = ""
        if res_val > 0.05:
            h_proc_res = (res_val / d) * proc_h
            h_out_res = max(5.0, min(30.0, (res_val / d) * 44.0))
            ribbon_res = make_ribbon(
                proc_x + proc_w, curr_proc_y, h_proc_res,
                card_out_x, y_out_res + 26 - h_out_res / 2, h_out_res
            )
            curr_proc_y += h_proc_res

        # Status Neraca
        is_balanced = abs(res_val) < 0.1
        balance_label = "● Neraca Seimbang 100%" if is_balanced else f"⚠️ Selisih Neraca: {res_val:.1f} kg"
        balance_color = "#10b981" if is_balanced else "#f59e0b"

        # Template HTML & SVG Lengkap (Almaty Style)
        svg = f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 22px; color: #1e293b; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; box-shadow: 0 4px 25px -4px rgba(0, 0, 0, 0.07);">
            <!-- HEADER DIAGRAM ALMATY STYLE -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #e2e8f0; padding-bottom: 14px;">
                <div>
                    <h3 style="margin: 0; font-size: 19px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                        <span>📊 Material Flow Analysis (MFA) — Model Sirkularitas Almaty</span>
                    </h3>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px;">
                        CV Teknika Prima Raya • Visualisasi Neraca Aliran Massa Pelat Fabrikasi &amp; Putaran Sisa Remnant
                    </div>
                </div>
                <div>
                    <span style="background: #f1f5f9; border: 1px solid #cbd5e1; padding: 6px 14px; border-radius: 8px; font-size: 13px; font-weight: 700; color: #0f172a;">
                        Total Beban Masukan (D): {self.total_input_kg:.1f} kg
                    </span>
                </div>
            </div>

            <!-- SVG CANVAS -->
            <svg viewBox="0 0 {svg_w} {svg_h}" style="width: 100%; height: auto; overflow: visible;">
                <defs>
                    <!-- Gradien Pita Aliran Almaty -->
                    <linearGradient id="alm_raw" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.6"/>
                        <stop offset="100%" stop-color="#6366f1" stop-opacity="0.45"/>
                    </linearGradient>
                    <linearGradient id="alm_reused" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#10b981" stop-opacity="0.7"/>
                        <stop offset="100%" stop-color="#6366f1" stop-opacity="0.45"/>
                    </linearGradient>
                    <linearGradient id="alm_prod" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#6366f1" stop-opacity="0.45"/>
                        <stop offset="100%" stop-color="#0284c7" stop-opacity="0.7"/>
                    </linearGradient>
                    <linearGradient id="alm_rem" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#6366f1" stop-opacity="0.45"/>
                        <stop offset="100%" stop-color="#059669" stop-opacity="0.7"/>
                    </linearGradient>
                    <linearGradient id="alm_scrap" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#6366f1" stop-opacity="0.45"/>
                        <stop offset="100%" stop-color="#e11d48" stop-opacity="0.65"/>
                    </linearGradient>
                    <linearGradient id="alm_loss" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#6366f1" stop-opacity="0.35"/>
                        <stop offset="100%" stop-color="#64748b" stop-opacity="0.5"/>
                    </linearGradient>
                    <linearGradient id="alm_res" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#6366f1" stop-opacity="0.35"/>
                        <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.6"/>
                    </linearGradient>

                    <!-- Filter Bayangan Kartu Halus -->
                    <filter id="card-shadow" x="-8%" y="-12%" width="120%" height="130%">
                        <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.16"/>
                    </filter>
                    <style>
                        .alm-ribbon {{ transition: fill-opacity 0.2s ease; cursor: pointer; }}
                        .alm-ribbon:hover {{ fill-opacity: 0.9 !important; }}
                    </style>
                </defs>

                <!-- JALUR SIRKULARITAS ATAS (TOP CYCLED RESOURCES HIGHWAY — METODE ALMATY) -->
                {f'''
                <g>
                    <!-- Lintasan Racetrack Atas (Highway Band) -->
                    <path d="M {card_out_x + card_out_w} {y_out_r + 26}
                             C 1110 {y_out_r + 26}, 1110 46, 1000 46
                             L 180 46
                             C 80 46, 80 240, {card_in_x} 240
                             L {card_in_x} 265
                             C 55 265, 55 26, 180 26
                             L 1000 26
                             C 1135 26, 1135 {y_out_r + 26}, {card_out_x + card_out_w} {y_out_r + 26} Z"
                          fill="rgba(16, 185, 129, 0.12)" stroke="#10b981" stroke-width="1.8" stroke-dasharray="7,5"/>

                    <!-- Marka Arah Aliran Sirkular (Chevrons) -->
                    <text x="890" y="40" fill="#059669" font-size="14" font-weight="900">‹ ‹ ‹</text>
                    <text x="240" y="40" fill="#059669" font-size="14" font-weight="900">‹ ‹ ‹</text>

                    <!-- Badge Keterangan Sirkularitas Terpusat -->
                    <rect x="{proc_x - 120}" y="28" width="430" height="28" rx="14" fill="#064e3b" stroke="#10b981" stroke-width="1.5" filter="url(#card-shadow)"/>
                    <text x="{proc_x + proc_w/2}" y="46" fill="#a7f3d0" font-size="11" font-weight="800" text-anchor="middle">
                        ♻️ CYCLED RESOURCES: {r_val:.1f} kg REMNANT DISIMPAN &amp; DIPAKAI ULANG DI MO BERIKUTNYA
                    </text>
                </g>
                ''' if r_val > 0 else ''}

                <!-- PEMBATAS & JUDUL TAHAP PROSES (STAGE HEADERS) -->
                <text x="200" y="98" fill="#64748b" font-size="12" font-weight="800" text-anchor="middle" letter-spacing="0.8">MASUKAN (INPUT)</text>
                <text x="{proc_x + proc_w/2}" y="98" fill="#64748b" font-size="12" font-weight="800" text-anchor="middle" letter-spacing="0.8">PEMROSESAN (PROCESSING)</text>
                <text x="{card_out_x + card_out_w/2}" y="98" fill="#64748b" font-size="12" font-weight="800" text-anchor="middle" letter-spacing="0.8">KELUARAN AKHIR (OUTPUT / SINKS)</text>

                <!-- Garis Pembatas Tahap Vertikal Halus -->
                <line x1="385" y1="110" x2="385" y2="480" stroke="#e2e8f0" stroke-width="1.5" stroke-dasharray="5,5"/>
                <line x1="760" y1="110" x2="760" y2="480" stroke="#e2e8f0" stroke-width="1.5" stroke-dasharray="5,5"/>

                <!-- PITA ALIRAN HALUS (RIBBONS) -->
                {f'<path class="alm-ribbon" d="{ribbon_raw}" fill="url(#alm_raw)"/>' if ribbon_raw else ''}
                {f'<path class="alm-ribbon" d="{ribbon_reused}" fill="url(#alm_reused)"/>' if ribbon_reused else ''}
                {f'<path class="alm-ribbon" d="{ribbon_p}" fill="url(#alm_prod)"/>' if ribbon_p else ''}
                {f'<path class="alm-ribbon" d="{ribbon_r}" fill="url(#alm_rem)"/>' if ribbon_r else ''}
                {f'<path class="alm-ribbon" d="{ribbon_s}" fill="url(#alm_scrap)"/>' if ribbon_s else ''}
                {f'<path class="alm-ribbon" d="{ribbon_l}" fill="url(#alm_loss)"/>' if ribbon_l else ''}
                {f'<path class="alm-ribbon" d="{ribbon_res}" fill="url(#alm_res)"/>' if ribbon_res else ''}

                <!-- === KOLOM 1: KARTU MASUKAN (INPUT CARDS) === -->
                <!-- Kartu Masukan Pelat Baru -->
                {f'''
                <g filter="url(#card-shadow)">
                    <rect x="{card_in_x}" y="{y_card_raw}" width="{card_in_w}" height="{card_in_h}" rx="10" fill="#0f172a" stroke="#2563eb" stroke-width="2"/>
                    <text x="{card_in_x + 14}" y="{y_card_raw + 21}" fill="#93c5fd" font-size="11" font-weight="700">📦 PELAT BARU (I_baru)</text>
                    <text x="{card_in_x + 14}" y="{y_card_raw + 42}" fill="#ffffff" font-size="15" font-weight="800">{raw_val:.1f} kg <tspan font-size="12" fill="#93c5fd" font-weight="600">({(raw_val/d)*100:.1f}%)</tspan></text>
                </g>
                ''' if raw_val > 0 else ''}

                <!-- Kartu Masukan Remnant Reusable -->
                {f'''
                <g filter="url(#card-shadow)">
                    <rect x="{card_in_x}" y="{y_card_reused}" width="{card_in_w}" height="{card_in_h}" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
                    <text x="{card_in_x + 14}" y="{y_card_reused + 21}" fill="#6ee7b7" font-size="11" font-weight="700">♻️ INPUT REMNANT (I_ulang)</text>
                    <text x="{card_in_x + 14}" y="{y_card_reused + 42}" fill="#ffffff" font-size="15" font-weight="800">{reused_val:.1f} kg <tspan font-size="12" fill="#6ee7b7" font-weight="600">({(reused_val/d)*100:.1f}%)</tspan></text>
                </g>
                ''' if reused_val > 0 else f'''
                <g opacity="0.6">
                    <rect x="{card_in_x}" y="{y_card_reused}" width="{card_in_w}" height="{card_in_h}" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4"/>
                    <text x="{card_in_x + 14}" y="{y_card_reused + 21}" fill="#94a3b8" font-size="10" font-weight="700">♻️ INPUT REMNANT (I_ulang)</text>
                    <text x="{card_in_x + 14}" y="{y_card_reused + 42}" fill="#64748b" font-size="13" font-weight="600">0.0 kg (Siklus Awal)</text>
                </g>
                '''}

                <!-- === KOLOM 2: KARTU PUSAT TRANSFORMASI (PROCESSING CARD) === -->
                <g filter="url(#card-shadow)">
                    <rect x="{proc_x}" y="{proc_y}" width="{proc_w}" height="{proc_h}" rx="14" fill="#0f172a" stroke="#6366f1" stroke-width="2.5"/>
                    <!-- Header Card -->
                    <text x="{proc_x + proc_w/2}" y="{proc_y + 26}" fill="#a5b4fc" font-size="12" font-weight="800" text-anchor="middle" letter-spacing="0.5">🏭 PEMOTONGAN FABRIKASI</text>
                    <text x="{proc_x + proc_w/2}" y="{proc_y + 45}" fill="#94a3b8" font-size="11" text-anchor="middle">Proses Transformasi MO</text>
                    <!-- Angka Utama -->
                    <text x="{proc_x + proc_w/2}" y="{proc_y + 88}" fill="#ffffff" font-size="28" font-weight="900" text-anchor="middle">{self.total_input_kg:.1f} kg</text>
                    <!-- Sub-badge -->
                    <rect x="{proc_x + 25}" y="{proc_y + 102}" width="{proc_w - 50}" height="22" rx="11" fill="rgba(99, 102, 241, 0.25)" stroke="#6366f1" stroke-width="1"/>
                    <text x="{proc_x + proc_w/2}" y="{proc_y + 117}" fill="#c7d2fe" font-size="10" font-weight="700" text-anchor="middle">Total Massa Diproses (D)</text>
                    <!-- Indikator Neraca -->
                    <text x="{proc_x + proc_w/2}" y="{proc_y + 148}" fill="{balance_color}" font-size="11" font-weight="700" text-anchor="middle">{balance_label}</text>
                </g>

                <!-- === KOLOM 3: KARTU KELUARAN (OUTPUT CARDS — ALMATY STYLE) === -->
                <!-- Kartu 1: Produk Jadi (P) -->
                <g filter="url(#card-shadow)">
                    <rect x="{card_out_x}" y="{y_out_p}" width="{card_out_w}" height="{card_out_h}" rx="10" fill="#0f172a" stroke="#0ea5e9" stroke-width="2"/>
                    <text x="{card_out_x + 14}" y="{y_out_p + 20}" fill="#7dd3fc" font-size="11" font-weight="700">⚙️ PRODUK JADI (P)</text>
                    <text x="{card_out_x + 14}" y="{y_out_p + 40}" fill="#ffffff" font-size="14" font-weight="800">{p_val:.1f} kg <tspan font-size="11" fill="#7dd3fc" font-weight="700">• {self.yield_pct:.1f}%</tspan></text>
                </g>

                <!-- Kartu 2: Remnant Reusable (R) -->
                <g filter="url(#card-shadow)">
                    <rect x="{card_out_x}" y="{y_out_r}" width="{card_out_w}" height="{card_out_h}" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
                    <text x="{card_out_x + 14}" y="{y_out_r + 20}" fill="#6ee7b7" font-size="11" font-weight="700">♻️ REMNANT REUSABLE (R)</text>
                    <text x="{card_out_x + 14}" y="{y_out_r + 40}" fill="#ffffff" font-size="14" font-weight="800">{r_val:.1f} kg <tspan font-size="11" fill="#6ee7b7" font-weight="700">• {self.remnant_pct:.1f}%</tspan></text>
                </g>

                <!-- Kartu 3: Scrap Fisik (S) -->
                <g filter="url(#card-shadow)">
                    <rect x="{card_out_x}" y="{y_out_s}" width="{card_out_w}" height="{card_out_h}" rx="10" fill="#0f172a" stroke="#f43f5e" stroke-width="2"/>
                    <text x="{card_out_x + 14}" y="{y_out_s + 20}" fill="#fda4af" font-size="11" font-weight="700">🗑️ SCRAP FISIK (S)</text>
                    <text x="{card_out_x + 14}" y="{y_out_s + 40}" fill="#ffffff" font-size="14" font-weight="800">{s_val:.1f} kg <tspan font-size="11" fill="#fda4af" font-weight="700">• {self.scrap_pct:.1f}%</tspan></text>
                </g>

                <!-- Kartu 4: Kerf Loss (L) -->
                <g filter="url(#card-shadow)">
                    <rect x="{card_out_x}" y="{y_out_l}" width="{card_out_w}" height="{card_out_h}" rx="10" fill="#0f172a" stroke="#94a3b8" stroke-width="2"/>
                    <text x="{card_out_x + 14}" y="{y_out_l + 20}" fill="#cbd5e1" font-size="11" font-weight="700">💨 KERF LOSS (L)</text>
                    <text x="{card_out_x + 14}" y="{y_out_l + 40}" fill="#ffffff" font-size="14" font-weight="800">{l_val:.1f} kg <tspan font-size="11" fill="#cbd5e1" font-weight="700">• {self.loss_pct:.1f}%</tspan></text>
                </g>

                <!-- Kartu 5: Residual Neraca (Hanya jika ada selisih) -->
                {f'''
                <g filter="url(#card-shadow)">
                    <rect x="{card_out_x}" y="{y_out_res}" width="{card_out_w}" height="{card_out_h}" rx="10" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
                    <text x="{card_out_x + 14}" y="{y_out_res + 20}" fill="#fde68a" font-size="11" font-weight="700">⚠️ RESIDUAL NERACA</text>
                    <text x="{card_out_x + 14}" y="{y_out_res + 40}" fill="#ffffff" font-size="14" font-weight="800">{res_val:.1f} kg <tspan font-size="11" fill="#fde68a" font-weight="700">• Selisih</tspan></text>
                </g>
                ''' if res_val > 0.05 else ''}
            </svg>

            <!-- KARTU INDIKATOR KPI BAWAH (METRIK STANDAR MFA) -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e8f0;">
                <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.5px;">Material Yield (P/D)</div>
                    <div style="font-size: 24px; font-weight: 900; color: #0284c7; margin-top: 4px;">{self.yield_pct:.1f}%</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 2px;">{self.product_output_kg:.1f} kg komponen jadi</div>
                </div>
                <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; font-weight: 700; color: #047857; text-transform: uppercase; letter-spacing: 0.5px;">Potensi Remnant (R/D)</div>
                    <div style="font-size: 24px; font-weight: 900; color: #059669; margin-top: 4px;">{self.remnant_pct:.1f}%</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 2px;">{self.remnant_output_kg:.1f} kg sisa layak pakai</div>
                </div>
                <div style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; font-weight: 700; color: #be123c; text-transform: uppercase; letter-spacing: 0.5px;">Scrap Fisik (S/D)</div>
                    <div style="font-size: 24px; font-weight: 900; color: #e11d48; margin-top: 4px;">{self.scrap_pct:.1f}%</div>
                    <div style="font-size: 12px; color: #475569; margin-top: 2px;">{self.scrap_output_kg:.1f} kg siap timbang &amp; jual</div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.5px;">Kehilangan Proses (L/D)</div>
                    <div style="font-size: 24px; font-weight: 900; color: #64748b; margin-top: 4px;">{self.loss_pct:.1f}%</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 2px;">{self.loss_kg:.1f} kg celah potong (kerf)</div>
                </div>
            </div>
        </div>
        """
        return svg

    # Aksi Pengisian Cepat Sesuai Bab 15 Panduan Sistem
    def action_load_demo_benchmark(self):
        """Memuat Data Acuan Standar Bab 15.1: MO A (100 kg input -> 72 kg produk, 20 kg remnant, 6 kg scrap, 2 kg loss)."""
        self.write({
            'name': 'MFA Data Acuan Simulasi MO A (Bab 15.1)',
            'raw_input_kg': 100.0,
            'reused_input_kg': 0.0,
            'product_output_kg': 72.0,
            'remnant_output_kg': 20.0,
            'scrap_output_kg': 6.0,
            'loss_kg': 2.0,
            'notes': 'Data acuan simulasi Bab 15.1 Panduan Sistem Odoo 19: Pelat MS 3 mm (100 kg bahan baru). Residual 0.0 kg.',
        })
        return True

    def action_load_demo_reuse(self):
        """Memuat Data Acuan Pemakaian Ulang Bab 15.2: MO B (8 kg input remnant R1 -> 5.5 kg produk, 2 kg anak, 0.5 kg scrap)."""
        self.write({
            'name': 'MFA Data Acuan Pemakaian Ulang MO B (Bab 15.2)',
            'raw_input_kg': 0.0,
            'reused_input_kg': 8.0,
            'product_output_kg': 5.5,
            'remnant_output_kg': 2.0,
            'scrap_output_kg': 0.5,
            'loss_kg': 0.0,
            'notes': 'Data acuan simulasi Bab 15.2 Panduan Sistem: Pemakaian ulang potongan R1 (8.0 kg input ulang). Menghasilkan anak R1A (2.0 kg).',
        })
        return True

    def action_load_from_mo(self):
        """Menarik data aktual dari Manufacturing Order yang dipilih."""
        self.ensure_one()
        if not self.production_id:
            raise UserError(_("Pilih 'Manufacturing Order (MO)' terlebih dahulu!"))
        mo = self.production_id

        # Total bahan baku yang dikonsumsi
        raw_consumed = sum(m.quantity for m in mo.move_raw_ids if m.state == 'done')
        if raw_consumed == 0:
            raw_consumed = sum(m.product_uom_qty for m in mo.move_raw_ids)

        # Total produk jadi yang dihasilkan
        prod_done = sum(m.quantity for m in mo.move_finished_ids if m.state == 'done' and m.product_id == mo.product_id)
        if prod_done == 0:
            prod_done = mo.product_qty

        # Potongan yang terkait dengan MO
        remnant_cuts = self.env['tpr.remnant.cut'].search([('production_id', '=', mo.id)])
        reusable_cuts = remnant_cuts.filtered(lambda c: c.inspection_result == 'reusable' or (c.state == 'quarantine' and c.inspection_result != 'scrap'))
        scrap_cuts = remnant_cuts.filtered(lambda c: c.inspection_result == 'scrap')

        rem_kg = sum(c.weight_kg for c in reusable_cuts)
        scrap_kg = sum(c.weight_kg for c in scrap_cuts)

        # Hitung loss dari selisih jika ada
        known_out = prod_done + rem_kg + scrap_kg
        loss_kg = max(0.0, raw_consumed - known_out)

        self.write({
            'name': f"MFA — {mo.name} ({mo.product_id.name})",
            'raw_input_kg': raw_consumed,
            'reused_input_kg': 0.0,
            'product_output_kg': prod_done,
            'remnant_output_kg': rem_kg,
            'scrap_output_kg': scrap_kg,
            'loss_kg': loss_kg,
            'notes': f"Dihitung otomatis dari transaksi MO {mo.name} ({len(remnant_cuts)} potongan sisa terhubung).",
        })
        return True
