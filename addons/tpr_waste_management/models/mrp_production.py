# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    remnant_cut_ids = fields.One2many(
        'tpr.remnant.cut',
        'production_id',
        string='Catatan Sisa Potongan (Remnants)',
        help='Sisa potongan atau scrap pelat yang dihasilkan dari proses produksi MO ini'
    )
    remnant_count = fields.Integer(
        string='Jumlah Potongan Sisa',
        compute='_compute_remnant_count'
    )

    @api.depends('remnant_cut_ids')
    def _compute_remnant_count(self):
        for prod in self:
            prod.remnant_count = len(prod.remnant_cut_ids)

    def action_view_remnant_cuts(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('tpr_waste_management.action_tpr_remnant_cut')
        action['domain'] = [('production_id', '=', self.id)]
        action['context'] = {
            'default_production_id': self.id,
            'default_company_id': self.company_id.id,
        }
        return action
