# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_plate_material = fields.Boolean(
        string='Material Pelat / Lembaran',
        default=False,
        help='Centang jika produk ini merupakan material pelat atau lembaran logam'
    )
    material_family_id = fields.Many2one(
        'tpr.material.family',
        string='Keluarga Material',
        ondelete='restrict'
    )
    material_grade_id = fields.Many2one(
        'tpr.material.grade',
        string='Grade Material',
        domain="[('family_id', '=', material_family_id)]",
        ondelete='restrict'
    )
    material_thickness_id = fields.Many2one(
        'tpr.material.thickness',
        string='Ketebalan Nominal',
        ondelete='restrict'
    )
    nominal_thickness_mm = fields.Float(
        string='Tebal (mm)',
        related='material_thickness_id.value',
        store=True,
        readonly=False
    )
    standard_length_mm = fields.Float(
        string='Panjang Standar (mm)',
        help='Panjang lembaran pelat standar pabrikan dalam milimeter'
    )
    standard_width_mm = fields.Float(
        string='Lebar Standar (mm)',
        help='Lebar lembaran pelat standar pabrikan dalam milimeter'
    )

    def calculate_theoretical_weight_kg(self, length_mm, width_mm, thickness_mm=None, density=None):
        """
        Menghitung estimasi berat teoritis (kg) berdasarkan dimensi (mm) dan densitas (g/cm³).
        Formula: (Panjang [mm] * Lebar [mm] * Tebal [mm] * Densitas [g/cm³]) / 1.000.000
        Contoh: Pelat Baja Karbon 1000 x 500 x 6 mm @ 7.85 g/cm³ = 23.55 kg
        """
        self.ensure_one()
        th = thickness_mm if thickness_mm is not None else self.nominal_thickness_mm
        dens = density or (self.material_family_id.density if self.material_family_id else 7.85)
        if not (length_mm and width_mm and th and dens):
            return 0.0
        return (length_mm * width_mm * th * dens) / 1000000.0


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Delegate helper call to template
    def calculate_theoretical_weight_kg(self, length_mm, width_mm, thickness_mm=None, density=None):
        self.ensure_one()
        return self.product_tmpl_id.calculate_theoretical_weight_kg(
            length_mm=length_mm,
            width_mm=width_mm,
            thickness_mm=thickness_mm,
            density=density
        )
