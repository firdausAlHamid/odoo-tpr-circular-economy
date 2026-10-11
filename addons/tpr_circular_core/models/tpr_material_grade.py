# -*- coding: utf-8 -*-
from odoo import models, fields


class TprMaterialGrade(models.Model):
    _name = 'tpr.material.grade'
    _description = 'Grade Material Pelat'
    _order = 'family_id, name'

    name = fields.Char(string='Grade Material', required=True)
    family_id = fields.Many2one(
        'tpr.material.family',
        string='Keluarga Material',
        required=True,
        ondelete='restrict'
    )
    standard_spec = fields.Char(
        string='Standar / Spesifikasi',
        help='Contoh: JIS G3101, ASTM A36, DIN EN 10025-2'
    )
    description = fields.Text(string='Keterangan')
    company_id = fields.Many2one(
        'res.company',
        string='Perusahaan',
        default=lambda self: self.env.company
    )
    active = fields.Boolean(string='Aktif', default=True)

    def _compute_display_name(self):
        for record in self:
            if record.family_id:
                record.display_name = f"{record.family_id.code} - {record.name}"
            else:
                record.display_name = record.name
