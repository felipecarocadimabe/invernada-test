from odoo import models, fields


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
