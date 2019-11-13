from odoo import models, fields, api
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_rut = fields.Char(
        'Rut Facturación'
    )

    acteco_id = fields.Many2one(
        'acteco',
        'Actividad Económica'
    )

    branch_office_sii_code = fields.Char(
        'Código Sucursal SII'
    )

    @api.model
    @api.depends('invoice_rut')
    @api.returns('self')
    def format_text(self):
        data = self.invoice_rut
        data = re.replace(r'/[^0-9k]/g', '', data)
        self.invoice_rut = data
        return self
