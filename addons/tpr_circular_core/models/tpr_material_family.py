# -*- coding: utf-8 -*-
from odoo import models, fields


class TprMaterialFamily(models.Model):
    _name = 'tpr.material.family'
    _description = 'Keluarga Material Pelat'
    _order = 'name'

    name = fields.Char(string='Nama Keluarga Material', required=True, translate=True)
    code = fields.Char(string='Kode Singkat', required=True, size=10)
    density = fields.Float(
        string='Massa Jenis / Densitas (g/cm³)',
        default=7.85,
        digits=(6, 4),
        help='Massa jenis material, misalnya 7.85 g/cm³ untuk baja karbon (Carbon Steel), 7.93 untuk SUS304'
    )
    description = fields.Text(string='Keterangan')
    raw_product_id = fields.Many2one(
        'product.product',
        string='Produk Bahan Baru Standar',
        help='Produk pelat baru standar yang mewakili keluarga material ini'
    )
    remnant_product_id = fields.Many2one(
        'product.product',
        string='Produk Sisa Potongan (Remnant)',
        help='Produk stok untuk menampung sisa potongan yang dapat digunakan kembali'
    )
    scrap_product_id = fields.Many2one(
        'product.product',
        string='Produk Scrap Fisik',
        help='Produk stok untuk menampung sisa pelat yang dialokasikan sebagai scrap fisik'
    )
    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        default=lambda self: self.env.company
    )
    active = fields.Boolean(string='Aktif', default=True)

    _code_company_uniq = models.Constraint(
        'unique(code, company_id)',
        'Kode keluarga material harus unik per perusahaan!',
    )
