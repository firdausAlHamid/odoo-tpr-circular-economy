# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TprMaterialThickness(models.Model):
    _name = 'tpr.material.thickness'
    _description = 'Ketebalan Nominal Pelat'
    _order = 'value asc'

    value = fields.Float(
        string='Ketebalan (mm)',
        required=True,
        digits=(6, 2),
        help='Ketebalan nominal dalam milimeter (mm)'
    )
    unit = fields.Selection(
        [('mm', 'mm')],
        string='Satuan',
        default='mm',
        required=True
    )
    name = fields.Char(
        string='Label Ketebalan',
        compute='_compute_name',
        store=True,
        readonly=False
    )
    description = fields.Char(string='Keterangan')
    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        default=lambda self: self.env.company
    )
    active = fields.Boolean(string='Aktif', default=True)

    @api.depends('value', 'unit')
    def _compute_name(self):
        for record in self:
            if record.value:
                # Format to clean float without trailing zero if integer
                val_str = f"{record.value:.1f}".rstrip('0').rstrip('.') if record.value % 1 == 0 else f"{record.value:.2f}".rstrip('0')
                record.name = f"{val_str} {record.unit or 'mm'}"
            else:
                record.name = ''

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name or f"{record.value} mm"
