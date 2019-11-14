from odoo import models, fields, api
import json


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
    def get_emitter_data(self):
        return {
            'RUTEmisor': self.invoice_rut,
            'RznSoc': self.name,
            'GiroEmis': self.acteco_id.activity,
            'Acteco': self.acteco_id.code,
            'DirOrigen': self.street,
            'CmnaOrigen': self.city,
            'Telefono': self.phone,
            'CdgSIISucur': self.branch_office_sii_code

        }

    @api.model
    def get_receiver_data(self):
        substring = self.acteco_id.activity
        if len(substring) > 40:
            substring = self.acteco_id.activity[0:35]
        return {
            'RUTRecep': self.invoice_rut,
            'RznSocRecep': self.name,
            'GiroRecep': substring,
            'DirRecep': self.street,
            'CmnaRecep': self.city

        }

